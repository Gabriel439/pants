# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.base.build_file_aliases             import BuildFileAliases
from pants.contrib.haskell.tasks.stack_bench   import StackBench
from pants.contrib.haskell.tasks.stack_build   import StackBuild
from pants.contrib.haskell.tasks.stack_ghci    import StackGhci
from pants.contrib.haskell.tasks.stack_haddock import StackHaddock
from pants.contrib.haskell.tasks.stack_install import StackInstall
from pants.contrib.haskell.tasks.stack_run     import StackRun
from pants.contrib.haskell.tasks.stack_test    import StackTest
from pants.contrib.haskell.targets.hackage     import Hackage
from pants.contrib.haskell.targets.cabal       import Cabal
from pants.contrib.haskell.targets.stackage    import Stackage
from pants.goal.task_registrar                 import TaskRegistrar

def build_file_aliases():
  return BuildFileAliases.create(
    targets ={
      'hackage' : Hackage,
      'cabal'   : Cabal,
      'stackage': Stackage,
    }
  )

def register_goals():
  TaskRegistrar(name='stack-bench'  , action=StackBench  ).install('criterion')
  TaskRegistrar(name='stack-build'  , action=StackBuild  ).install('compile')
  TaskRegistrar(name='stack-ghci'   , action=StackGhci   ).install('repl')
  TaskRegistrar(name='stack-haddock', action=StackHaddock).install('doc')
  TaskRegistrar(name='stack-install', action=StackInstall).install('binary')
  TaskRegistrar(name='stack-run'    , action=StackRun    ).install('run')
  TaskRegistrar(name='stack-test'   , action=StackTest   ).install('test')
