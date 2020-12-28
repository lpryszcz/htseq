#!/bin/bash
#
# Build manylinux wheels for HTSeq. Based on the example at
# <https://github.com/pypa/python-manylinux-demo>
#
# It is best to run this in a fresh clone of the repository!
#
# Run this within the repository root:
#   docker run --rm -v $(pwd):/io quay.io/pypa/manylinux2010_x86_64 /io/buildwheels.sh
#
# The wheels will be put into the wheelhouse/ subdirectory.
#
# For interactive tests:
#   docker run -it -v $(pwd):/io quay.io/pypa/manylinux2010_x86_64 /bin/bash

set -xeuo pipefail

echo "Destroy wheelhouse and source (keep tests and docs)"
rm -rf /io/wheelhouse /io/build /io/src /io/HTSeq /io/dist

echo "Uninstall packages and (some) deps"
pip uninstall numpy pysam matplotlib Cython wheel HTSeq

echo "PYTHON_VERSION: ${PYTHON_VERSION}"
export PYTHON_FDN=cp$(echo ${PYTHON_VERSION} | sed 's/\.//')
PYBINS="/opt/python/${PYTHON_FDN}*/bin"
for PYBIN in ${PYBINS}; do
    echo "PYBIN = ${PYBIN}"

    echo "Install from Pypi..."
    ${PYBIN}/pip install HTSeq
    if [ $? != 0 ]; then
      exit 1
    fi
done
echo "Done installing"

# Test after install?
