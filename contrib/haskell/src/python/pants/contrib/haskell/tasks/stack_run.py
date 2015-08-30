# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os
import subprocess

from pants.contrib.haskell.tasks.stack_task import StackTask

class StackRun(StackTask):
  @classmethod
  def register_options(cls, register):
    super(StackRun, cls).register_options(register)
    register('--executable', help='Name of the executable to run.')

  def execute(self):
    with self.stack_task("install") as dir:
      executable = os.path.join(dir, "bin", self.get_options().executable)
      subprocess.check_call(executable)
