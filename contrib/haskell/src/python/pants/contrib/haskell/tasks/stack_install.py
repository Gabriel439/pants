# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os
import subprocess
import tempfile

from pants.backend.core.tasks.task                 import Task
from pants.contrib.haskell.targets.hackage_package import HackagePackage
from pants.contrib.haskell.targets.haskell_package import HaskellPackage
from pants.util.contextutil                        import temporary_file

class StackInstall(Task):
  def execute(self):
    def is_hackage_package(target):
      return isinstance(target, HackagePackage)

    for target in self.context.target_roots:
      if isinstance(target, HaskellPackage):
        hackage_packages = filter(is_hackage_package, target.dependencies)
        with temporary_file() as handle:
          handle.write("flags: {}\n")
          handle.write("packages: []\n")
          if hackage_packages:
            handle.write("extra-deps:\n")
            for pkg in hackage_packages:
              handle.write("- " + pkg.package + "-" + pkg.version)
          else:
            handle.write("extra-deps: []\n")
          handle.write("resolver: " + target.resolver + "\n")
          handle.close()
          stack_yaml_path = handle.name
          print("")
          subprocess.check_call(["stack", "--stack-yaml=" + stack_yaml_path, "build", target.package])
