import unittest

from util.functions import get_max_value, smart_round, remove_redundant_spacing
from examples.stats.data_for_charts import simple_funnel_data, rich_funnel_data


class TestGetMaxValue(unittest.TestCase):
    def test_for_simple_funnel(self):
        expected = 110
        received = get_max_value(simple_funnel_data)
        self.assertEqual(expected, received)

    def test_for_rich_funnel(self):
        expected = 80
        received = get_max_value(rich_funnel_data)
        self.assertEqual(expected, received)
        expected = 110
        received = get_max_value(rich_funnel_data, sum_secondary=True)
        self.assertEqual(expected, received)


class TestSmartRound(unittest.TestCase):
    def test_smart_round(self):
        number = 12345
        expected = 12000
        received = smart_round(number)
        self.assertEqual(expected, received)
        count = 3
        number = -12345
        expected = -12300
        received = smart_round(number, count)
        self.assertEqual(expected, received)
        number = 12345
        expected = 13000
        received = smart_round(number, upper=True)
        self.assertEqual(expected, received)


class TestRemoveRedundantSpacing(unittest.TestCase):
    def test_remove_redundant_spacing(self):
        text = 'a  b\n\nc'
        expected = 'a  b\nc'
        received = remove_redundant_spacing(text)
        self.assertEqual(expected, received)


if __name__ == '__main__':
    unittest.main()
