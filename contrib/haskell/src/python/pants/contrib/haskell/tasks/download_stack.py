# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.tasks.haskell import HaskellTask

class DownloadStack(HaskellTask):
  """Retrieve Haskell's `stack` package manager tool"""
  def execute(self):
    x = self.stack_binary_path
