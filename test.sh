#!/bin/bash

PYTHON=python3

###############################################################################

set -e

CLEAN=0
COUNT_ONLY=0
CONDA=0
PYTEST_ARGS=
VENV_DIR=.venv

while getopts ":coae:k:" OPTION; do
    echo "$OPTION"
    case $OPTION in
        o)
	  COUNT_ONLY=1
          ;;
        c)
          CLEAN=1
          ;;
	a)
	  CONDA=1
	  ;;
        e)
	  VENV_DIR=$OPTARG
          ;;
	k)
	  PYTEST_ARGS="${PYTEST_ARGS} -k $OPTARG"
	  ;;
        \?)
          echo "Usage: $0 [-c]"
          ;;
    esac
done
shift $((OPTIND -1))


if [ x$CLEAN = x1 ]; then
    rm -rf build/
fi

if [ x$CONDA = x1 ]; then
  source /opt/anaconda/bin/activate
  conda activate scanpy
  PYTHON=python
  PIP=pip
  PYTEST=pytest
else
  PYTHON=$VENV_DIR/bin/python
  PIP=$VENV_DIR/bin/pip
  PYTEST=$VENV_DIR/bin/pytest

  if [ ! -d $VENV_DIR ]; then
      $PYTHON -m venv $VENV_DIR
      $VENV_DIR/bin/pip install -U pip wheel numpy
  fi
fi

#$PYTHON setup.py build
$PIP install --use-feature=in-tree-build .[htseq-qa,test]

if [ x$CONDA = x1 ]; then
  if [ x$COUNT_ONLY = x1 ]; then
    $PYTEST test/test_htseq-count.py ${PYTEST_ARGS}
  else
    $PYTEST test ${PYTEST_ARGS}
  fi
else
  if [ x$COUNT_ONLY = x1 ]; then
    PATH=${VENV_DIR}/bin:${PATH} $PYTEST test/test_htseq-count.py ${PYTEST_ARGS}
  else
    PATH=${VENV_DIR}/bin:${PATH} $PYTEST test ${PYTEST_ARGS}
  fi
fi
