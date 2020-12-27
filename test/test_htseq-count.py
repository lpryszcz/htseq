import os
import subprocess as sp
import pytest

tests = [
    {'call': [
        'htseq-count',
        '--version']},
    {'call': [
        'htseq-count',
        'example_data/bamfile_no_qualities.sam',
        'example_data/bamfile_no_qualities.gtf',
        ],
     'expected_fn': 'example_data/bamfile_no_qualities.tsv'},
    {'call': [
        'htseq-count',
        '-c', 'test_output.tsv',
        'example_data/bamfile_no_qualities.sam',
        'example_data/bamfile_no_qualities.gtf',
        ],
     'expected_fn': 'example_data/bamfile_no_qualities.tsv'},
    # Testing multiple cores on travis makes a mess
    #{'call': [
    #    'htseq-count',
    #    '-n', '2',
    #    'example_data/bamfile_no_qualities.sam',
    #    'example_data/bamfile_no_qualities.gtf',
    #    ],
    # 'expected_fn': 'example_data/bamfile_no_qualities.tsv'},
    {'call': [
        'htseq-count',
        'example_data/bamfile_no_qualities.bam',
        'example_data/bamfile_no_qualities.gtf',
        ],
     'expected_fn': 'example_data/bamfile_no_qualities.tsv'},
    {'call': [
        'htseq-count',
        '-m', 'intersection-nonempty',
        '--nonunique', 'none',
        '--secondary-alignments', 'score',
        '--supplementary-alignments', 'score',
        'example_data/yeast_RNASeq_excerpt_withNH.sam',
        'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
        ],
     'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts.tsv'},
    {'call': [
        'htseq-count',
        '-m', 'intersection-nonempty',
        '--nonunique', 'none',
        '--secondary-alignments', 'score',
        '--supplementary-alignments', 'score',
        '--feature-query', 'gene_id == "YPR036W-A"',
        'example_data/yeast_RNASeq_excerpt_withNH.sam',
        'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
        ],
     'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_YPR036W-A.tsv'},
    {'call': [
        'htseq-count-barcodes',
        '-m', 'intersection-nonempty',
        '--nonunique', 'none',
        '--secondary-alignments', 'score',
        '--supplementary-alignments', 'score',
        'example_data/yeast_RNASeq_excerpt_withbarcodes.sam',
        'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
        ],
     'expected_fn': 'example_data/yeast_RNASeq_excerpt_withbarcodes.tsv'},
    {'call': [
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
     'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_additional_attributes.tsv'},
    {'call': [
        'htseq-count',
        '-m', 'intersection-nonempty',
        '--nonunique', 'fraction',
        '--secondary-alignments', 'score',
        '--supplementary-alignments', 'score',
        'example_data/yeast_RNASeq_excerpt_withNH.sam',
        'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
        ],
     'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_nonunique_fraction.tsv'},
    {'call': [
        'htseq-count',
        '-m', 'intersection-nonempty',
        '--nonunique', 'all',
        '--secondary-alignments', 'score',
        '--supplementary-alignments', 'score',
        'example_data/yeast_RNASeq_excerpt_withNH.sam',
        'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
        ],
     'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_nonunique.tsv'},
    {'call': [
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
     'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_twocolumns.tsv'},
    {'call': [
        'htseq-count',
        '-m', 'intersection-nonempty',
        '--nonunique', 'none',
        '--secondary-alignments', 'ignore',
        '--supplementary-alignments', 'score',
        'example_data/yeast_RNASeq_excerpt_withNH.sam',
        'example_data/Saccharomyces_cerevisiae.SGD1.01.56.gtf.gz',
        ],
     'expected_fn': 'example_data/yeast_RNASeq_excerpt_withNH_counts_ignore_secondary.tsv'},
    ]


# Run the tests
def test_htseq(data_folder):
    print('Testing htseq-count')

    for it, t in enumerate(tests):
        print('Test #'+str(it+1))
        expected_fn = t.get('expected_fn', None)
        call = t['call']

        # Replace with injected variable
        call = [x.replace('example_data/', data_folder) for x in call]
        if expected_fn is not None:
            expected_fn = expected_fn.replace('example_data/', data_folder)

        # local testing
        #call = ['python', 'HTSeq/scripts/count.py'] + call[1:]

        print(' '.join(call))
        output = sp.check_output(call).decode()

        if '-c' in call:
            output_fn = call[call.index('-c') + 1]
            with open(output_fn, 'r') as f:
                output = f.read()
        else:
            output_fn = None

        if expected_fn is None:
            if '--version' in call:
                print('version:', output)
            continue

        with open(expected_fn, 'r') as f:
            expected = f.read()

        try:
            assert output == expected
        except AssertionError:
            for out, exp in zip(output.split('\n'), expected.split('\n')):
                print(out, exp)
                if out != exp:
                    break

            raise
        finally:
            if output_fn is not None:
                os.remove(output_fn)

if __name__ == '__main__':
    test_htseq('example_data/')
