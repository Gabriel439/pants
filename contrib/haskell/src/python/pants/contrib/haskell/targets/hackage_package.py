# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.targets.haskell_package import HaskellPackage

class HackagePackage(HaskellPackage):
  def __init__(self, version, **kwargs):
    self.version = version
    super(HackagePackage, self).__init__(**kwargs)
