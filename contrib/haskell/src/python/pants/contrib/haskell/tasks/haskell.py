# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import gzip
import os
import requests

from pants.backend.core.tasks.task import Task
from pants.base.exceptions import TaskError
from pants.util.dirutil import safe_mkdir
from pants.util.memo import memoized_property

class HaskellTask(Task):
  def __init__(self, *args, **kwargs):
    super(Task, self).__init__(*args, **kwargs)

    v = { 'version' : '0.1.3.1' }
    self.binary_name   = 'stack-%(version)s-x86_64-osx'    % v
    self.gzip_name     = 'stack-%(version)s-x86_64-osx.gz' % v
    self.gzip_url      = 'https://github.com/commercialhaskell/stack/releases/download/v%(version)s/stack-%(version)s-x86_64-osx.gz' % v

  @memoized_property
  def haskell_workdir(self):
    safe_mkdir(self.workdir)
    return self.workdir
  
  @memoized_property
  def stack_gzip_path(self):
    stack_gzip_path = os.path.join(self.haskell_workdir, self.gzip_name)

    gzip_exists = os.path.isfile(stack_gzip_path)
    if not gzip_exists:
      r = requests.get(self.gzip_url)
      if not r.ok:
        print("\nFailed to download the Haskell `stack` tool from: {}".format(gzip_url))
        raise(TaskError())

      with open(stack_gzip_path, 'wb') as f:
        f.write(r.content)

    return stack_gzip_path

  @memoized_property
  def stack_binary_path(self):
    stack_binary_path = os.path.join(self.haskell_workdir, self.binary_name)

    binary_exists = os.path.isfile(stack_binary_path)
    if not binary_exists:
      with open(stack_binary_path, 'wb') as outfile:
        with gzip.open(self.stack_gzip_path, 'rb') as infile:
          outfile.write(infile.read())
    os.chmod(stack_binary_path, 0544)

    return stack_binary_path
