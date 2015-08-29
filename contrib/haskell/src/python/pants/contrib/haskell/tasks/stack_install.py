# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os
import subprocess
import tempfile

from pants.backend.core.tasks.task import Task
from pants.contrib.haskell.targets.stackage_package import StackagePackage
from pants.util.contextutil import temporary_file

class StackInstall(Task):
  def execute(self):
    def is_stackage_package(target):
      return isinstance(target, StackagePackage)

    for target in self.context.target_roots:
      if isinstance(target, StackagePackage):
        with temporary_file() as handle:
          handle.write("flags: {}\n")
          handle.write("packages: []\n")
          handle.write("extra-deps: []\n")
          handle.write("resolver: " + target.resolver + "\n")
          handle.close()
          stack_yaml_path = handle.name
          print("")
          subprocess.check_call(["stack", "--stack-yaml=" + stack_yaml_path, "build", target.package])
