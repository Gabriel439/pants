# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.targets.haskell_package import HaskellPackage

class CabalPackage(HaskellPackage):
  def __init__(self, path = None, **kwargs):
    self.path = path
    super(CabalPackage, self).__init__(**kwargs)
