import unittest
from generate_page import extract_title


class TestPageFunctions(unittest.TestCase):
    
    def test_extract_title(self):
        md = "# This is a title\n\nThis is some content."
        expected_title = "This is a title"
        self.assertEqual(extract_title(md), expected_title)
    
    def test_extract_title_no_title(self):
        md = "This is some content."
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue("Title not found" in str(context.exception))
    
    def test_extract_title_empty(self):
        md = ""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue("Title not found" in str(context.exception))

    def test_extract_title_leading_spaces(self):
        md = "#   This is a title\n\nThis is some content."
        expected_title = "This is a title"
        self.assertEqual(extract_title(md), expected_title)

if __name__ == '__main__':
    unittest.main()