# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.tasks.stack_task import StackTask

class StackHaddock(StackTask):
  """Generate Haddock documentation for the given Haskell target

  The Haddock documentation will be located at:

  `path/to/target/.stack-work/dist/<arch>/<cabal-version>/doc/html/<package-name>/index.html`
  """
  def execute(self):
    for dir in self.stack_task("haddock"):
      pass
