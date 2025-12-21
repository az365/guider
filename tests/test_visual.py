import unittest

from examples.stats.data_for_charts import simple_funnel_data
from visual import Size2d


class TestChartSize(unittest.TestCase):
    def test_chart_size(self):
        axis_width = 50
        chart_size = Size2d(500, 200)
        bars_count = len(simple_funnel_data)
        row_height = chart_size.y / bars_count
        row_frame_size = Size2d(chart_size.x, row_height)
        bar_frame_size = Size2d(chart_size.x - axis_width, row_height)
        mark_size = Size2d(axis_width, row_height)
        received = f'{row_frame_size} = {mark_size} + {bar_frame_size}'
        expected = '500x40.0px = 50x40.0px + 450x40.0px'
        self.assertEqual(expected, received)


if __name__ == '__main__':
    unittest.main()
