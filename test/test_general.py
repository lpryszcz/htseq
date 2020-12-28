import pytest
import sys
import os
import glob
import distutils.util

build_dir = "build/lib.%s-%s" % (distutils.util.get_platform(), sys.version[0:3])
sys.path.insert(0, os.path.join(os.getcwd(), build_dir))


def test_import():
    print('Import HTSeq')
    try:
        import HTSeq
    except ModuleNotFoundError:
        print('cwd:', os.getcwd())
        print('build_dir:', build_dir)
        print('PYTHONPATH:', sys.path)


def test_version():
    print('Test version')
    import HTSeq
    print(HTSeq.__version__)
    print('Test passed')
