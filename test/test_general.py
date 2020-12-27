import pytest
import sys
import os
import glob
import distutils.util

build_dir = "build/lib.%s-%s" % (distutils.util.get_platform(), sys.version[0:3])

sys.path.insert(0, os.path.join(os.getcwd(), build_dir))
import HTSeq


def test_version():
    print('Test version')
    print(HTSeq.__version__)
    print('Test passed')
