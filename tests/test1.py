import unittest

from wrappers.common_wrapper import CommonWrapper
from viewers.serial_viewer import SerialViewer


class TestCommonWrapper(unittest.TestCase):
    def test_common_wrapper(self):
        d = dict(a=1, b=2)
        w = CommonWrapper(d)

        expected_repr = "({'a': 1, 'b': 2})"
        self.assertEqual(expected_repr, repr(w))

    def test_second_common_wrapper(self):
        d = dict(a=1, b=2)
        w = CommonWrapper(d)
        w2 = CommonWrapper(w)

        expected_repr = "(({'a': 1, 'b': 2}))"
        self.assertEqual(expected_repr, repr(w2))

        expected_props = {'a': 1, 'b': 2}
        received_props = w2.get_props(including_protected=True, add=[])
        self.assertEqual(expected_props, received_props)

    def test_yaml(self):
        d = dict(a=1, b=2)
        line = 'a: 1\nb: 2\n'
        viewer = SerialViewer(use_tech_names=True, skip_empty=True)
        parsed = viewer.parse(line)
        self.assertEqual(d, parsed.get_raw_object())
        yaml_repr = viewer.get_view(parsed).get_yaml()
        self.assertEqual(line, yaml_repr)


if __name__ == '__main__':
    unittest.main()
