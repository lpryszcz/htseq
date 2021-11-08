import pytest
import numpy as np
import sys
import os
import glob
import distutils.util
from pathlib import Path
import unittest
import pytest
import conftest

build_dir = "build/lib.%s-%s" % (distutils.util.get_platform(), sys.version[0:3])

sys.path.insert(0, os.path.join(os.getcwd(), build_dir))
import HTSeq


data_folder = conftest.get_data_folder()


class TestStretchVector(unittest.TestCase):
    def test_init(self):
        sv = HTSeq.StretchVector(typecode='d')
        self.assertEqual(sv.ivs, [])
        self.assertEqual(sv.stretches, [])

    def test_setitem_number(self):
        sv = HTSeq.StretchVector(typecode='d')

        # Set initial stretch
        sv[560] = 4.5
        self.assertEqual(len(sv.ivs), 1)
        self.assertEqual(len(sv.stretches), 1)
        np.testing.assert_almost_equal(
            sv.stretches[0],
            np.ones(1, np.float32) * 4.5,
        )

        # Overwrite
        sv[560] = 4
        self.assertEqual(len(sv.ivs), 1)
        self.assertEqual(len(sv.stretches), 1)
        np.testing.assert_almost_equal(
            sv.stretches[0],
            np.ones(1, np.float32) * 4,
        )

    def test_setitem_slice(self):
        sv = HTSeq.StretchVector(typecode='d')

        # Set initial stretch
        sv[100: 300] = 4.5
        self.assertEqual(len(sv.ivs), 1)
        self.assertEqual(len(sv.stretches), 1)
        np.testing.assert_almost_equal(
            sv.stretches[0],
            np.ones(200, np.float32) * 4.5,
        )

        # Set overlapping stretch
        sv[50:250] = 3
        self.assertEqual(len(sv.ivs), 1)
        self.assertEqual(len(sv.stretches), 1)
        np.testing.assert_almost_equal(
            sv.stretches[0][:200],
            np.ones(200, np.float32) * 3,
        )
        np.testing.assert_almost_equal(
            sv.stretches[0][200:],
            np.ones(50, np.float32) * 4.5,
        )

        # Set new stretch
        sv[400: 450] = np.arange(50)
        self.assertEqual(len(sv.ivs), 2)
        self.assertEqual(len(sv.stretches), 2)
        np.testing.assert_almost_equal(
            sv.stretches[1],
            np.arange(50).astype(np.float32),
        )

        # Set overlapping stretch
        sv[430: 450] = np.arange(20)
        self.assertEqual(len(sv.ivs), 2)
        self.assertEqual(len(sv.stretches), 2)
        np.testing.assert_almost_equal(
            sv.stretches[1][-20:],
            np.arange(20).astype(np.float32),
        )

    def test_getitem_number(self):
        sv = HTSeq.StretchVector(typecode='d')

        # Set initial stretch
        sv[560] = 4.5
        self.assertEqual(sv[560], 4.5)
        self.assertEqual(sv[580], None)

        sv[400: 450] = np.arange(50)
        res = sv[350: 430]
        self.assertEqual(len(res.ivs), 1)
        self.assertEqual(len(res.stretches), 1)
        np.testing.assert_almost_equal(
            res.stretches[0],
            np.arange(30).astype(np.float32),
        )

    def test_todense(self):
        sv = HTSeq.StretchVector(typecode='d')
        sv[450: 455] = 6.7
        sv[460: 465] = 1.7
        res = sv.todense()
        np.testing.assert_almost_equal(
            res,
            np.array([6.7] * 5 + [np.nan] * 5 + [1.7] * 5).astype(np.float32),
        )


if __name__ == '__main__':

    suite = TestStretchVector()
    suite.test_init()
