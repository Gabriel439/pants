# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.targets.haskell_package import HaskellPackage

class CabalPackage(HaskellPackage):
  """A local or remote `cabal` package

  If you provide the `path` field then this target points to the source archive
  located at `path`.  Otherwise, this target points to a `cabal` source tree anchored
  at the current directory.
  """

  def __init__(self, remote = None, **kwargs):
    """
    :param str remote: Optional path to a remote source archive in TAR or ZIP format
    """
    self.path = path
    super(CabalPackage, self).__init__(**kwargs)
