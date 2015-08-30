# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants_test.pants_run_integration_test import PantsRunIntegrationTest

class StackHaddockIntegrationTest(PantsRunIntegrationTest):

  def test_stack_haddock_integration(self):
    path = 'contrib/haskell/examples/src/haskell/new-template'
    self.assert_success(self.run_pants(['doc', path]))
