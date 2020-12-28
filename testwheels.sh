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

echo "PYTHON_VERSION: ${PYTHON_VERSION}"
export PYTHON_FDN=cp$(echo ${PYTHON_VERSION} | sed 's/\.//')
PYBINS="/opt/python/${PYTHON_FDN}*/bin"
for PYBIN in ${PYBINS}; do
    echo "Testing $PYBIN"
    ${PYBIN}/pip install pytest
    ${PYBIN}/pip install HTSeq --no-index -f /io/wheelhouse
    (cd /io; ls; DOCKER_IMAGE='' OS_NAME='centos-6' PYTHON=${PYBIN}/python PATH=${PYBIN}:${PATH} ./.ci_test.sh)
    if [ $? != 0 ]; then
        exit 1
    fi
done

