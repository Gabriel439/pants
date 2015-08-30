# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.base.address                            import SyntheticAddress
from pants.contrib.haskell.targets.hackage_package import HackagePackage
from pants.contrib.haskell.tasks.stack_build       import StackBuild
from pants_test.tasks.task_test_base               import TaskTestBase

class StackTaskTest(TaskTestBase):

  address = SyntheticAddress.parse

  @classmethod
  def task_type(cls):
    return StackBuild

  def test_make_stack_yaml(self):
    stack_build = self.create_task(self.context())

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
    actual_yaml = stack_build.make_stack_yaml(discrimination)

    self.assertEqual(expected_yaml, actual_yaml)
