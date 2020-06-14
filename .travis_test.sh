#!/bin/bash
# Wheels are already tested in docker image
if [ $DOCKER_IMAGE ]; then
  docker run --rm -v $(pwd):/io $DOCKER_IMAGE /io/testwheels.sh
  exit $?
fi

if [ "$TRAVIS_OS_NAME" == 'osx' ]; then
  export PATH="$HOME/miniconda/bin:$PATH"
  source $HOME/miniconda/bin/activate
  conda activate travis
  #PYTHON="$HOME/miniconda/bin/python$CONDA_PY"
  PYTHON=$(which python)
else
  PYTHON=${PYTHON:-python}
fi

echo "python: ${PYTHON}"

echo 'Running tests...'

echo 'General tests...'
${PYTHON} test/test_general.py
if [ $? != 0 ]; then
    exit 1
fi
echo 'done!'

echo 'Doctests...'
${PYTHON} test/test.py
if [ $? != 0 ]; then
    exit 1
fi
echo 'done!'

echo 'htseq-count...'
${PYTHON} test/test_htseq-count.py
if [ $? != 0 ]; then
    exit 1
fi
echo 'done!'
