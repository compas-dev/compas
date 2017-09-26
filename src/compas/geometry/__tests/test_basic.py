import unittest

from compas.geometry import basic


class TestReturns(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sum_vectors(self):
        m = 10
        n = 3
        vectors = [[j for j in range(n)] for i in range(m)]
        r0 = basic.sum_vectors(vectors, axis=0)
        r1 = basic.sum_vectors(vectors, axis=1)
        self.assertEqual(len(r0), n)
        self.assertEqual(len(r1), m)

    def test_norm_vector(self):
        pass


if __name__ == '__main__':
    unittest.main()
