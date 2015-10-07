# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from pants.contrib.haskell.tasks.stack_task import StackTask


class StackGhci(StackTask):
  """Load the given Haskell target into the `ghci` REPL"""

  def execute(self):
    for dir in self.stack_task("ghci"):
      pass
