# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.base.build_file_aliases                  import BuildFileAliases
from pants.contrib.haskell.tasks.stack_install      import StackInstall
from pants.contrib.haskell.targets.hackage_package  import HackagePackage
from pants.contrib.haskell.targets.stackage_package import StackagePackage
from pants.goal.task_registrar                      import TaskRegistrar

def build_file_aliases():
  return BuildFileAliases.create(
    targets ={
      'stackage_package': StackagePackage,
      'hackage_package' : HackagePackage,
    }
  )

def register_goals():
  TaskRegistrar(name='stack-build', action=StackInstall).install('compile')
