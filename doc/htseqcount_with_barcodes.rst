.. _htseqcount_with_barcodes:

.. program:: htseq-count-barcodes


*******************************************************************************************
``htseq-count-barcodes``: counting reads with cell barcodes and UMIs
*******************************************************************************************

This script is similar to ``htseq-count``, but is designed to operate on a single SAM/BAM/CRAM file that contains reads from many cells, distinguished by a cell barcode in the read name and possibly a unique molecular identifier (UMI).

To keep the documentation simple, this page does not repeat the explanations found for ``htseq-count`` at :ref:`htseqcount` and focuses on the differences instead.

* Unlike ``htseq-count``, only one read file is accepted.

* No multicore support is available ATM. Because barcoded, position-sorted BAM files are not trivially parallelizable, this feature is a little challenging to implement, however pull requests (PRs) on Github are welcome.

* The main target for this script are BAM files produced by 10X Genomics' ``cellranger`` pipeline. If you have a different application and would like to use ``htseq-count-barcodes``, please open an issue on Github and we'll be happy to consider adding it.
