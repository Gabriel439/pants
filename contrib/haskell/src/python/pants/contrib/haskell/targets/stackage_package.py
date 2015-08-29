# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.base.target import Target

class StackagePackage(Target):
  def __init__(self, package, resolver, **kwargs):
    """
    :param str package : The name of the package (i.e. "network" or "containers")
    :param str resolver: The `stack` resolver (i.e. "lts-3.1" or "nightly-2015-08-29")
    """
    self.package  = package
    self.resolver = resolver
    super(StackagePackage, self).__init__(**kwargs)
