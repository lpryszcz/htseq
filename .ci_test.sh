#!/bin/bash
# try and make wheels
if [ $DOCKER_IMAGE ]; then
  docker run --rm -v `pwd`:/io $DOCKER_IMAGE /io/testwheels.sh 
  if [ $? != 0 ]; then
      exit 1
  fi
  ls wheelhouse/
  if [ $? != 0 ]; then
      exit 1
  fi

# test normally
else
  if [ $OS_NAME == 'macos-latest' ]; then
    export PATH="$HOME/miniconda/bin:$PATH"
    source $HOME/miniconda/bin/activate
    conda activate ci
  fi

  pytest --doctest-glob="*.rst"
  if [ $? != 0 ]; then
      exit 1
  fi
fi
