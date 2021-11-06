import numpy as np


class StretchVector:
    _typecode_dict = {
        "d": np.float32,
        "i": np.int32,
        "l": np.int64,
        "O": object,
    }

    def __init__(self, typecode):
        self.typecode = typecode
        self.ivs = []
        self.stretches = []

    def _in_array(self, index):
        if len(self.stretches) == 0:
            return -1

        if isinstance(index, int):
            if (index < self.ivs[0]) or (index >= self.ivs[-1]):
                return -1
            for i, iv in enumerate(self.ivs):
                if index < iv.start:
                    return -1
                if index < iv.end:
                    return i

    def _add_stretch(self, start, end, value=None):
        from HTSeq import GenomicInterval

        for i, iv in enumerate(self.ivs):
            if start < iv.start:
                self.ivs.insert(
                    i,
                    GenomicInterval(start, end, "."),
                )
                self.stretches.insert(
                    i,
                    np.zeros(end - start, self._typecode_dict[self.typecode])
                )
                return i

        self.ivs.append(
            GenomicInterval(start, end, "."),
        )
        self.stretches.append(
            np.zeros(end - start, self._typecode_dict[self.typecode])
        )
        return len(self.ivs) - 1

    def __getitem__(self, index):
        from HTSeq import GenomicInterval

        if isinstance(index, int):
            # TODO
            pass

        elif isinstance(index, slice):
            # TODO
            pass

        elif isinstance(index, GenomicInterval):
            # TODO
            pass

    def __setitem__(self, index, value):
        from HTSeq import GenomicInterval

        if isinstance(index, int):
            idx_iv =self._in_array(index)
            if idx_iv == -1:
                idx_iv = self._add_stretch(index, index + 1)
            self.stretches[idx_iv][index - self.ivs[idx_iv].start] = value
            return

        elif isinstance(index, slice):
            # TODO
            pass

        elif isinstance(index, GenomicInterval):
            # TODO
            pass


