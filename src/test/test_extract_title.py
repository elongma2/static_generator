import unittest
from helper_func import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a title"
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title")
    
    def test_no_title(self):
        markdown = "This is not a title"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)
