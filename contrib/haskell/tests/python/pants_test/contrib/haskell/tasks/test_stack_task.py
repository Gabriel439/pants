# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.targets.hackage_package  import HackagePackage
from pants.contrib.haskell.targets.stackage_package import StackagePackage
from pants.contrib.haskell.tasks.stack_task         import StackTask
from pants_test.base_test                           import BaseTest

class StackTaskTest(BaseTest):

  def test_make_stack_yaml_for_stackage_package(self):
    pipes = self.make_target(
      spec        = '3rdparty:pipes',
      target_type = StackagePackage,
      package     = 'pipes',
      resolver    = 'lts-3.1',
    )

    expected_yaml = (
      "flags: {}\n"
      "packages: []\n"
      "extra-deps: []\n"
      "resolver: lts-3.1\n"
    )
    actual_yaml = StackTask.make_stack_yaml(pipes)

    self.assertEqual(expected_yaml, actual_yaml)

  def test_make_stack_yaml_for_hackage_package(self):
    promises = self.make_target(
      spec        = '3rdparty:promises',
      target_type = HackagePackage,
      package     = 'promises',
      version     = '0.2',
      resolver    = 'lts-3.1',
    )

    discrimination = self.make_target(
      spec         = '3rdparty:discrimination',
      target_type  = HackagePackage,
      package      = 'discrimination',
      version      = '0.1',
      dependencies = [promises],
      resolver     = 'lts-3.1',
    )

    expected_yaml = (
      "flags: {}\n"
      "packages: []\n"
      "extra-deps:\n"
      "- discrimination-0.1\n"
      "- promises-0.2\n"
      "resolver: lts-3.1\n"
    )
    actual_yaml = StackTask.make_stack_yaml(discrimination)

    self.assertEqual(expected_yaml, actual_yaml)
