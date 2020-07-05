# -*- coding: utf-8 -*-
import tempfile
import shutil
from contextlib import contextmanager

@contextmanager
def tempdir():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)
