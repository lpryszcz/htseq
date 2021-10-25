import os
import subprocess as sp
import unittest
import pytest

data_folder = 'example_data/'


class HTSeqCount(unittest.TestCase):
    def _run(self, t):
        expected_fn = t.get('expected_fn', None)
        call = t['call']

        # Replace with injected variable
        call = [x.replace('example_data/', data_folder) for x in call]
        if expected_fn is not None:
            expected_fn = expected_fn.replace('example_data/', data_folder)

        ## local testing
        #if call[0] == 'htseq-count':
        #    call = ['python', 'HTSeq/scripts/count.py'] + call[1:]
        #else:
        #    call = ['python', 'HTSeq/scripts/count_with_barcodes.py'] + call[1:]

        print(' '.join(call))
        output = sp.check_output(
                ' '.join(call),
                shell=True,
        ).decode()

        if '-c' in call:
            output_fn = call[call.index('-c') + 1]
            with open(output_fn, 'r') as f:
                output = f.read()
        else:
            output_fn = None

        if expected_fn is None:
            if '--version' in call:
                print('version:', output)
            return

        with open(expected_fn, 'r') as f:
            expected = f.read()

        try:
            self.assertEqual(output, expected)
        except AssertionError:
            print(f'Expected filename: {expected_fn}')
            for out, exp in zip(output.split('\n'), expected.split('\n')):
                print(out, exp)
                #if out != exp:
                #    break

            raise
        finally:
            if output_fn is not None:
                os.remove(output_fn)

    def test_version(self):
        self._run({
            'call': [
                'htseq-count',
                '--version'],
            })

    def test_simple(self):
        self._run({
            'call': [
                'htseq-count',
                'example_data/bamfile_no_qualities.sam',
                'example_data/bamfile_no_qualities.gtf',
            ],
            'expected_fn': 'example_data/bamfile_no_qualities.tsv',
            })

    def test_output_tsv(self):
        self._run({
            'call': [
                'htseq-count',
                '-c', 'test_output.tsv',
                'example_data/bamfile_no_qualities.sam',
                'example_data/bamfile_no_qualities.gtf',
                ],
        'expected_fn': 'example_data/bamfile_no_qualities.tsv',
        })

    # Testing multiple cores on travis makes a mess
    #{'call': [
    #    'htseq-count',
    #    '-n', '2',
    #    'example_data/bamfile_no_qualities.sam',
    #    'example_data/bamfile_no_qualities.gtf',
    #    ],
    # 'expected_fn': 'example_data/bamfile_no_qualities.tsv'},

    def test_no_qualities(self):
        self._run({
            'call': [
                'htseq-count',
                'example_data/bamfile_no_qualities.bam',
                'example_data/bamfile_no_qualities.gtf',
            ],
            'expected_fn': 'example_data/bamfile_no_qualities.tsv',
            })

    def test_intersection_nonempty(self):
        self._run({
            'call': [
                'htseq-count',
                '-m', 'intersection-nonempty',
                '--nonunique', 'none',
                '--secondary-alignments', 'score',
                '--supplementary-alignments', 'score',
                'example_data/yeast_RNASeq_excerpt_withNH.sam',
                'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
                ],
            'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts.tsv',
            })

    def test_feature_query(self):
        self._run({
            'call': [
                'htseq-count',
                '-m', 'intersection-nonempty',
                '--nonunique', 'none',
                '--secondary-alignments', 'score',
                '--supplementary-alignments', 'score',
                '--feature-query', '\'gene_id == "YPR036W-A"\'',
                'example_data/yeast_RNASeq_excerpt_withNH.sam',
                'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
                ],
            'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_YPR036W-A.tsv',
            })

    def test_barcodes(self):
        self._run({
            'call': [
                'htseq-count-barcodes',
                '-m', 'intersection-nonempty',
                '--nonunique', 'none',
                '--secondary-alignments', 'score',
                '--supplementary-alignments', 'score',
                'example_data/yeast_RNASeq_excerpt_withbarcodes.sam',
                'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
                ],
            'expected_fn': 'example_data/yeast_RNASeq_excerpt_withbarcodes.tsv',
            })

    def test_additional_attributes(self):
        self._run({
            'call': [
                'htseq-count',
                '-m', 'intersection-nonempty',
                '--nonunique', 'none',
                '--secondary-alignments', 'score',
                '--supplementary-alignments', 'score',
                '--additional-attr', 'gene_name',
                '--additional-attr', 'exon_number',
                'example_data/yeast_RNASeq_excerpt_withNH.sam',
                'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
                ],
            'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_additional_attributes.tsv',
            })

    def test_nonunique_fraction(self):
        self._run({
            'call': [
                'htseq-count',
                '-m', 'intersection-nonempty',
                '--nonunique', 'fraction',
                '--secondary-alignments', 'score',
                '--supplementary-alignments', 'score',
                'example_data/yeast_RNASeq_excerpt_withNH.sam',
                'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
                ],
            'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_nonunique_fraction.tsv',
            })

    def test_withNH(self):
        self._run({
            'call': [
                'htseq-count',
                '-m', 'intersection-nonempty',
                '--nonunique', 'all',
                '--secondary-alignments', 'score',
                '--supplementary-alignments', 'score',
                'example_data/yeast_RNASeq_excerpt_withNH.sam',
                'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
                ],
            'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_nonunique.tsv',
            })

    def test_twocolumns(self):
        self._run({
            'call': [
                'htseq-count',
                '-m', 'intersection-nonempty',
                '-i', 'gene_id',
                '--additional-attr', 'gene_name',
                '--nonunique', 'none',
                '--secondary-alignments', 'score',
                '--supplementary-alignments', 'score',
                'example_data/yeast_RNASeq_excerpt_withNH.sam',
                'example_data/yeast_RNASeq_excerpt_withNH.sam',
                'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
                ],
            'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_twocolumns.tsv',
            })

    def test_ignore_secondary(self):
        self._run({
            'call': [
                'htseq-count',
                '-m', 'intersection-nonempty',
                '--nonunique', 'none',
                '--secondary-alignments', 'ignore',
                '--supplementary-alignments', 'score',
                'example_data/yeast_RNASeq_excerpt_withNH.sam',
                'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
                ],
            'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_ignore_secondary.tsv',
            })


if __name__ == '__main__':

    suite = HTSeqCount()

    suite.test_version()
    suite.test_simple()
    suite.test_output_tsv()
    suite.test_no_qualities()
    suite.test_intersection_nonempty()
    suite.test_feature_query()
    suite.test_barcodes()
    suite.test_additional_attributes()
    suite.test_nonunique_fraction()
    suite.test_withNH()
    suite.test_twocolumns()
    suite.test_ignore_secondary()
