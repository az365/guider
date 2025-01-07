import unittest

from wrappers.common_wrapper import CommonWrapper


class TestCommonWrapper(unittest.TestCase):
    def test_common_wrapper(self):
        d = dict(a=1, b=2)
        w = CommonWrapper(d)

        expected_repr = "CommonWrapper({'a': 1, 'b': 2})"
        self.assertEqual(expected_repr, repr(w))

    def test_second_common_wrapper(self):
        d = dict(a=1, b=2)
        w = CommonWrapper(d)
        w2 = CommonWrapper(w)

        expected_repr = "CommonWrapper(CommonWrapper({'a': 1, 'b': 2}))"
        self.assertEqual(expected_repr, repr(w2))

        expected_props = {'a': 1, 'b': 2}
        received_props = w2.get_props(including_protected=True, add=[])
        self.assertEqual(expected_props, received_props)


if __name__ == '__main__':
    unittest.main()
