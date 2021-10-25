import numpy as np


class UnknownChrom(Exception):
    pass


def my_showwarning(message, category, filename, lineno=None, file=None,
                   line=None):
    sys.stderr.write("Warning: %s\n" % message)


def invert_strand(iv):
    iv2 = iv.copy()
    if iv2.strand == "+":
        iv2.strand = "-"
    elif iv2.strand == "-":
        iv2.strand = "+"
    else:
        raise ValueError("Illegal strand")
    return iv2


def _merge_counts(
        results,
        feature_attr,
        attributes,
        additional_attributes,
        sparse=False,
        dtype=np.float32,
        ):

    other_features = [
        ('__no_feature', 'empty'),
        ('__ambiguous', 'ambiguous'),
        ('__too_low_aQual', 'lowqual'),
        ('__not_aligned', 'notaligned'),
        ('__alignment_not_unique', 'nonunique'),
        ]
    fea_names = [fea for fea in feature_attr] + [fea[0] for fea in other_features]
    L = len(fea_names)
    n = len(results)
    if not sparse:
        table = np.zeros(
            (n, L),
            dtype=dtype,
        )
    else:
        from scipy.sparse import lil_matrix
        table = lil_matrix((n, L), dtype=dtype)

    fea_ids = [fea for fea in feature_attr] + [fea[1] for fea in other_features]
    for j, r in enumerate(results):
        countj = r['counts']
        for i, fn in enumerate(fea_ids):
            countji = countj[fn]
            if countji > 0:
                table[j, i] = countji

    if sparse:
        table = table.tocsr()

    feature_metadata = {
        'id': fea_names,
    }

    return {
        'feature_metadata': feature_metadata,
        'table': table,
    }


def _count_results_to_tsv(
        results,
        feature_attr,
        attributes,
        additional_attributes,
        output_filename,
        output_append,
        output_delimiter,
        ):

    # Print or write header??

    # Each feature is a row with feature id, additional attrs, and counts
    for ifn, fn in enumerate(feature_attr):
        fields = [fn] + attributes[fn] + [str(r['counts'][fn]) for r in results]
        line = output_delimiter.join(fields)
        if output_filename == '':
            print(line)
        else:
            omode = 'a' if output_append or (ifn > 0) else 'w'
            with open(output_filename, omode) as f:
                f.write(line)
                f.write('\n')

    # Add other features (unmapped, etc.)
    other_features = [
        ('__no_feature', 'empty'),
        ('__ambiguous', 'ambiguous'),
        ('__too_low_aQual', 'lowqual'),
        ('__not_aligned', 'notaligned'),
        ('__alignment_not_unique', 'nonunique'),
        ]
    pad = ['' for attr in additional_attributes]
    for title, fn in other_features:
        fields = [title] + pad + [str(r[fn]) for r in results]
        line = output_delimiter.join(fields)
        if output_filename == '':
            print(line)
        else:
            with open(output_filename, 'a') as f:
                f.write(line)
                f.write('\n')


def _count_table_to_sparse_mtx(
        filename,
        table,
        feature_metadata,
        sample_filenames,
        sparse=False,
        ):
    if not str(filename).endswith('.mtx'):
        raise ValueError('Matrix Marker filename should end with ".mtx"')

    try:
        from scipy.io import mmwrite
    except ImportError:
        raise ImportError('Install scipy for mtx support')

    if sparse:
        from scipy.sparse import csr_matrix
        table = csr_matrix(table)

    filename_pfx = str(filename)[:-4]
    filename_feature_meta = filename_pfx+'_features.tsv'
    filename_samples = filename_pfx+'_samples.tsv'

    # Write main matrix
    mmwrite(
        filename,
        table,
    )

    # Write input filenames
    with open(filename_samples, 'wt') as fout:
        for fn in sample_filenames:
            fout.write(fn+'\n')

    # Write feature metadata (ids and additional attributes)
    with open(filename_feature_meta, 'wt') as fout:
        nkeys = len(feature_metadata)
        for ik, key in enumerate(feature_metadata):
            if ik != nkeys - 1:
                f.write(key+'\t')
            else:
                f.write(key+'\n')
        nfeatures = len(feature_metadata[key])
        for i in range(nfeatures):
            for ik, key in enumerate(feature_metadata):
                if ik != nkeys - 1:
                    f.write(feature_metadata[key][i]+'\t')
                else:
                    f.write(feature_metadata[key][i]+'\n')


def _count_table_to_h5ad(
        filename,
        table,
        feature_metadata,
        sample_filenames,
        sparse=False,
        ):
    try:
        import anndata
    except ImportError:
        raise ImportError('Install the anndata package for h5ad support')

    # If they have anndata, they have scipy and pandas too
    import pandas as pd

    feature_metadata = pd.DataFrame(feature_metadata)
    feature_metadata.set_index(feature_metadata.columns[0], inplace=True)


    if sparse:
        from scipy.sparse import csr_matrix
        table = csr_matrix(table)

    adata = anndata.AnnData(
        X=table,
        obs=pd.DataFrame([], index=sample_filenames),
        var=feature_metadata,
    )
    adata.to_h5ad(filename)


def _count_table_to_loom(
        filename,
        table,
        feature_metadata,
        sample_filenames,
        sparse=False,
        ):

    try:
        import loompy
    except ImportError:
        raise ImportError('Install the loompy package for loom support')

    if sparse:
        from scipy.sparse import csr_matrix
        table = csr_matrix(table)

    layers = table.T
    row_attrs = feature_metadata
    col_attrs = {'_index': sample_filenames}
    loompy.create(
        filename,
        layers=layers,
        row_attrs=row_attrs,
        col_attrs=col_attrs,
    )
