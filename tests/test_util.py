import unittest

from util.functions import get_max_value
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


if __name__ == '__main__':
    unittest.main()
