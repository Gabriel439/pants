# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.contrib.haskell.targets.hackage_package  import HackagePackage
from pants.contrib.haskell.targets.local_package    import LocalPackage
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

    # We expect an empty `stack.yaml` because the `resolver` field uniquely determines
    # all Stackage dependencies.  We supply the actual package name (i.e. `pipes` in
    # this case) to the `stack` tool on the command line.
    expected_yaml = (
      "flags: {}\n"
      "packages: []\n"
      "extra-deps: []\n"
      "resolver: lts-3.1\n"
    )
    actual_yaml = StackTask.make_stack_yaml(pipes)

    self.assertEqual(actual_yaml, expected_yaml)

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

    self.assertEqual(actual_yaml, expected_yaml)

  def test_make_stack_yaml_for_local_package(self):
    newtemplate = self.make_target(
      spec        = 'src/haskell/new-template',
      target_type = LocalPackage,
      package     = 'new-template',
      resolver    = 'lts-3.1',
    )

    expected_yaml_header = [
      "flags: {}",
      "packages:",
    ]
    # We never use the contents of the local source tree directly.  We only pass the
    # path to the source tree to the `stack` tool, which does the rest
    expected_path_regex = "- .*?/src/haskell/new-template"
    expected_yaml_footer = [
      "extra-deps: []",
      "resolver: lts-3.1"
    ]
    actual_yaml = StackTask.make_stack_yaml(newtemplate).split("\n")

    self.assertEqual(len(actual_yaml), 6)
    self.assertEqual(actual_yaml[0:2], expected_yaml_header)
    self.assertRegexpMatches(actual_yaml[2], expected_path_regex)
    self.assertEqual(actual_yaml[3:5], expected_yaml_footer)