#!/bin/bash

PYTHON=python3

###############################################################################

set -e

CLEAN=0
COUNT_ONLY=0
PYTEST_ARGS=
VENV_DIR=.venv

while getopts ":coe:k:" OPTION; do
    echo "$OPTION"
    case $OPTION in
        o)
	  COUNT_ONLY=1
          ;;
        c)
          CLEAN=1
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

if [ ! -d $VENV_DIR ]; then
    $PYTHON -m venv $VENV_DIR
    $VENV_DIR/bin/pip install -U pip wheel numpy
fi

if [ x$CLEAN = x1 ]; then
    rm -rf build/
fi

#$VENV_DIR/bin/python setup.py build
$VENV_DIR/bin/pip install --use-feature=in-tree-build .[htseq-qa,test]
if [ x$COUNT_ONLY = x1 ]; then
  PATH=${VENV_DIR}/bin:${PATH} $VENV_DIR/bin/pytest test/test_htseq-count.py ${PYTEST_ARGS}
else
  PATH=${VENV_DIR}/bin:${PATH} $VENV_DIR/bin/pytest test ${PYTEST_ARGS}
fi

