# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.tasks.stack_task import StackTask

class StackTest(StackTask):
  def execute(self):
    with self.stack_task("test"):
      pass
