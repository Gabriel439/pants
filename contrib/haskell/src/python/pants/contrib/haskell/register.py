# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.base.build_file_aliases import BuildFileAliases
from pants.goal.task_registrar import TaskRegistrar

from pants.contrib.haskell.tasks.download_stack import DownloadStack

def build_file_aliases():
  return BuildFileAliases.create(
    targets ={
    }
  )

def register_goals():
  TaskRegistrar(name='download-stack', action=DownloadStack).install('download-stack')
