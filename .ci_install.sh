#!/bin/bash
# try and make wheels
if [ $DOCKER_IMAGE ]; then
  docker run --rm -v `pwd`:/io $DOCKER_IMAGE /io/buildwheels.sh 
  if [ $? != 0 ]; then
      exit 1
  fi
  ls wheelhouse/
  if [ $? != 0 ]; then
      exit 1
  fi

# compile normally
else
  if [ $TRAVIS_OS_NAME == 'macos-latest' ]; then
    export PATH="$HOME/miniconda/bin:$PATH"
    source $HOME/miniconda/bin/activate
    conda activate travis
  fi

  pip install -v '.[htseq-qa]'
  if [ $? != 0 ]; then
      exit 1
  fi
fi

# OSX makes wheels as well
if [ $TRAVIS_OS_NAME == 'macos-latest' ]; then
  mkdir wheelhouse
  pip wheel . -w wheelhouse/
  if [ $? != 0 ]; then
      exit 1
  fi
  #FIXME
  ls wheelhouse
fi

