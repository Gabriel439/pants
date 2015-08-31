# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os
import subprocess

from pants.contrib.haskell.tasks.stack_task import StackTask

class StackRun(StackTask):
  """Build and run an executable associated with the given Haskell target

  You must specify which executable to run using the `--run-stack-run-executable`
  option since Haskell projects may have more than one executable associated with
  them.
  """
  @classmethod
  def register_options(cls, register):
    super(StackRun, cls).register_options(register)
    register('--executable', help='Name of the executable to run.')

  def execute(self):
    for dir in self.stack_task("install"):
      executable = os.path.join(dir, "bin", self.get_options().executable)
      subprocess.check_call(executable)
