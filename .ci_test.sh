#!/bin/bash
if [ $OS_NAME == 'macos-latest' ]; then
  export PATH="$HOME/miniconda/bin:$PATH"
  source $HOME/miniconda/bin/activate
  conda activate ci
fi

pytest --doctest-glob="*.rst"
if [ $? != 0 ]; then
    exit 1
fi
