[![Build Status](https://travis-ci.org/htseq/htseq.svg?branch=master)](https://travis-ci.org/htseq/htseq)
[![Documentation Status](https://readthedocs.org/projects/htseq/badge/?version=master)](https://htseq.readthedocs.io)

# HTSeq
**DEVS**: https://github.com/htseq/htseq

**DOCS**: http://htseq.readthedocs.io

A Python library to facilitate processing and analysis of data
from high-throughput sequencing (HTS) experiments. A popular use of ``HTSeq``
is ``htseq-count``, a tool to quantify gene expression in RNA-Seq and similar
experiments.

## Requirements

To use ``HTSeq`` you will need:

-  ``Python 2.7`` or ``Python >= 3.5`` 
-  ``numpy``
-  ``pysam >= 0.9.0``

To run the ``htseq-qa`` script, you will also need:

-  ``matplotlib >=1.4``

Both **Linux** and **OSX** are supported and binaries are provided on for many
Linux and OSX versions. A source package which should not require ``Cython``
nor ``SWIG`` is provided for all other cases. To **build** the package completely
from source, you will **also** need:

-  ``Cython >=0.29.5``
-  ``SWIG >=3.0.8``

which are required for performance reasons.

**Windows is not officially supported** as we don't have access to a Continuous
Integration Windows machine that supports ``pysam``. Please do **not** open an
issue asking to support Windows installers: we do not know how to do that and 
do not have the bandwidth to learn. However, if you are interested in giving it
a try yourself, we are happy to provide as much support as we can.

## Installation

### PIP

To install directly from PyPI:

```bash
pip install HTSeq
```

To install a specific version:

```bash
pip install 'HTSeq==0.14.0'
```

If this fails, please install all dependencies first:

```bash
pip install 'matplotlib>=1.4'
pip install Cython
pip install 'pysam>=0.9'
pip install HTSeq
```

**NOTE**: ``pysam==0.9.0`` has a bug so that ``pip Cython`` is
**required** at installation. ``pysam>=0.10.0`` should build without
Cython.

### setup.py (distutils/setuptools)

Install the dependencies with your favourite tool (``pip``, ``conda``,
etc.).

To install ``HTSeq`` itself, run:

```bash
python setup.py build install
```

## Authors
- Since 2016: Fabio Zanini @ http://fabilab.org.
- 2020-2015: Simon Anders, Wolfgang Huber
