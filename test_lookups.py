import unittest
from xlextract.__init__ import XLExtract

# GLOBAL VARIABLES
test_excel_file: str = "inventory.xlsx"
test_sheet: str = "test"

class TestLookups(unittest.TestCase):

    def test_left_lookup(self):
        test_table = XLExtract(test_excel_file, test_sheet, "HEADER2")
        test_table.LLookup()
        self.assertEqual(test_table.value, "HEADER1", "Invalid Left Lookup Value")
        
    def test_right_lookup(self):
        test_table = XLExtract(test_excel_file, test_sheet, "HEADER1")
        test_table.RLookup()
        self.assertEqual(test_table.value, "HEADER2", "Invalid Right Lookup Value")

    def test_bottom_lookup(self):
        test_table = XLExtract(test_excel_file, test_sheet, "HEADER1")
        test_table.BLookup()
        self.assertEqual(test_table.value, "Value1", "Invalid Bottom Lookup Value")

    def test_table_lookup(self):
        test_table = XLExtract(test_excel_file, test_sheet, "HEADER1")
        test_table.TLookup()
        self.assertEqual(len(test_table.value), 2, "List (number of rows) not correct")
        self.assertEqual(list(test_table.value[0].keys()), ['HEADER1','HEADER2'], "Invalid headers detected")
        self.assertEqual(list(test_table.value[0].values()), ['Value1', 'Value2'], "Invalid row1 values detected")
        self.assertEqual(list(test_table.value[1].values()), ['Value11', 'Value22'], "Invalid row2 values detected")

if __name__ == '__main__':
    unittest.main()