# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.tasks.stack_task import StackTask

class StackGhci(StackTask):
  def execute(self):
    for dir in self.stack_task("ghci"):
      pass
