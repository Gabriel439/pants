# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.base.exceptions                  import TaskError
from pants.contrib.haskell.targets.hackage  import Hackage
from pants.contrib.haskell.targets.cabal    import Cabal
from pants.contrib.haskell.targets.stackage import Stackage
from pants.contrib.haskell.tasks.stack_task import StackTask
from pants_test.base_test                   import BaseTest

class StackTaskTest(BaseTest):

  def test_make_stack_yaml_for_stackage(self):
    pipes = self.make_target(
      spec        = '3rdparty:pipes',
      target_type = Stackage,
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

  def test_make_stack_yaml_for_hackage(self):
    promises = self.make_target(
      spec        = '3rdparty:promises',
      target_type = Hackage,
      package     = 'promises',
      version     = '0.2',
      resolver    = 'lts-3.1',
    )

    discrimination = self.make_target(
      spec         = '3rdparty:discrimination',
      target_type  = Hackage,
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

  def test_resolver_validation(self):
    promises = self.make_target(
      spec        = '3rdparty:promises',
      target_type = Hackage,
      package     = 'promises',
      version     = '0.2',
      resolver    = 'lts-3.0',
    )

    discrimination = self.make_target(
      spec         = '3rdparty:discrimination',
      target_type  = Hackage,
      package      = 'discrimination',
      version      = '0.1',
      dependencies = [promises],
      resolver     = 'lts-3.1',
    )

    self.assertRaises(TaskError, StackTask.make_stack_yaml, discrimination)

  def test_make_stack_yaml_for_remote_cabal(self):
    stack = self.make_target(
      spec        = '3rdparty:stack',
      target_type = Cabal,
      package     = 'stack',
      resolver    = 'lts-3.1',
      path        = 'https://github.com/commercialhaskell/stack/archive/v0.1.3.1.tar.gz',
    )

    expected_yaml = (
      "flags: {}\n"
      "packages:\n"
      "- https://github.com/commercialhaskell/stack/archive/v0.1.3.1.tar.gz\n"
      "extra-deps: []\n"
      "resolver: lts-3.1\n"
    )
    actual_yaml = StackTask.make_stack_yaml(stack)

    self.assertEqual(actual_yaml, expected_yaml)

  def test_make_stack_yaml_for_local_cabal(self):
    newtemplate = self.make_target(
      spec        = 'src/haskell/new-template',
      target_type = Cabal,
      package     = 'new-template',
      resolver    = 'lts-3.1',
    )

    expected_yaml_header = [
      "flags: {}",
      "packages:",
    ]
    # We never use the contents of the cabal source tree directly.  We only pass the
    # path to the source tree to the `stack` tool, which does the rest
    #
    # We match against a regex because the auto-generated path will be something like:
    #
    #     "- /private/var/vp0hm......4lcCsM_BUILD_ROOT/src/haskell/new-template"
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
