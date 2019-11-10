from tests import mock_data
from tests import file1_output
from src.grid_data import GridData
from src.site_data import SiteData
import json
import unittest


class ParseTest(unittest.TestCase):

    def test_site1(self):
        d = json.loads(mock_data.site1)
        s = SiteData(d)
        self.assertEqual(s.get_dict(), mock_data.site1_dict)

    def test_site2(self):
        d = json.loads(mock_data.site2)
        s = SiteData(d)
        self.assertEqual(s.get_dict(), mock_data.site2_dict)

    def test_site3(self):
        d = json.loads(mock_data.site3)
        s = SiteData(d)
        self.assertEqual(s.get_dict(), mock_data.site3_dict)

    def test_grid(self):
        s = GridData()
        s.load_json_string(mock_data.testgrid)
        self.assertEqual(s.get_grid_state(), mock_data.testgrid_list)

    def test_file(self):
        gd = GridData()
        gd.load_file('tests/file1.save')
        self.assertEqual(file1_output.filetest_out, gd.get_grid_state())


if __name__ == '__main__':
    unittest.main()
