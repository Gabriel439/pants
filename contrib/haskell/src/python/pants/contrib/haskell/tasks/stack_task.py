# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os
import subprocess

from pants.backend.core.tasks.task                 import Task
from pants.base.build_environment                  import get_buildroot
from pants.contrib.haskell.targets.local_package   import LocalPackage
from pants.contrib.haskell.targets.hackage_package import HackagePackage
from pants.contrib.haskell.targets.haskell_package import HaskellPackage
from pants.util.contextutil                        import temporary_dir
from pants.util.dirutil                            import safe_mkdir

class StackTask(Task):
  @staticmethod
  def is_hackage_package(target):
    return isinstance(target, HackagePackage)

  @staticmethod
  def is_local_package(target):
    return isinstance(target, LocalPackage)

  @staticmethod
  def make_stack_yaml(target):
    packages = [target] + target.dependencies

    hackage_packages = filter(StackTask.is_hackage_package, packages)
    local_packages   = filter(StackTask.is_local_package  , packages)

    yaml = "flags: {}\n"

    if local_packages:
      yaml += "packages:\n"
      for pkg in local_packages:
        path = os.path.join(get_buildroot(), pkg.target_base)
        yaml += "- " + path + "\n"
    else:
      yaml += "packages: []\n"

    if hackage_packages:
      yaml += "extra-deps:\n"
      for pkg in hackage_packages:
        yaml += "- " + pkg.package + "-" + pkg.version + "\n"
    else:
      yaml += "extra-deps: []\n"

    yaml += "resolver: " + target.resolver + "\n"

    return yaml

  def stack_task(self, command):
    for target in self.context.target_roots:
      if isinstance(target, HaskellPackage):
        yaml = StackTask.make_stack_yaml(target)

        with temporary_dir() as dir:
          stack_yaml_path = os.path.join(dir, "stack.yaml")
          with open(stack_yaml_path, 'w') as handle:
            handle.write(yaml)

          bin_path = os.path.join(dir, "bin")
          safe_mkdir(bin_path)

          try:
            subprocess.check_call(["stack", "--verbosity", "error", "--local-bin-path", bin_path, "--install-ghc", "--stack-yaml=" + stack_yaml_path, command, target.package])
            yield dir
          except:
            print("")
            print("Contents of " + stack_yaml_path + ":")
            print("")
            print("```")
            print(yaml)
            print("```")
            raise
