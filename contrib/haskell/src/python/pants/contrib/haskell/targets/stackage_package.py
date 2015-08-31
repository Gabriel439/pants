# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.targets.haskell_package import HaskellPackage

class StackagePackage(HaskellPackage):
  """A package hosted on Stackage

  You never need to use this target as a dependency since the `resolver` field already
  specifies all Stackage-related dependencies.  The only purpose of this target is if
  you wish to directly compile/test/bench/install/etc. a Stackage package.
  """
  pass
