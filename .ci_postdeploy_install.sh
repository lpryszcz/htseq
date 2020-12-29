#!/bin/bash
if [ $OS_NAME == 'macos-latest' ]; then
  export PATH="$HOME/miniconda/bin:$PATH"
  source $HOME/miniconda/bin/activate
  conda activate ci
fi

echo "Destroy wheelhouse and source (keep tests and docs)"
rm -rf wheelhouse build src HTSeq dist

echo "Uninstall packages and (some) deps"
pip uninstall HTSeq

echo "Install from Pypi..."
pip install --no-binary ":all:" "HTSeq==$(cat VERSION)"
if [ $? != 0 ]; then
  exit 1
fi
echo "Done installing"
