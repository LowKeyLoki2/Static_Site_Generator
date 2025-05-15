import unittest
from markdown_to_blocks import markdown_to_blocks

# filepath: /home/jonathan/Coding/Static_Site_Generator/src/test_markdown_to_blocks.py

class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_single_paragraph(self):
        md = "This is a simple paragraph."
        self.assertEqual(markdown_to_blocks(md), ["This is a simple paragraph."])

    def test_multiple_paragraphs(self):
        md = """This is the first paragraph.

This is the second paragraph.

This is the third paragraph."""
        expected = [
            "This is the first paragraph.",
            "This is the second paragraph.",
            "This is the third paragraph."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_paragraph_with_line_breaks(self):
        md = """This is the first line of a paragraph.
This is the second line.

This is a new paragraph."""
        expected = [
            "This is the first line of a paragraph.\nThis is the second line.",
            "This is a new paragraph."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_paragraph_with_leading_spaces(self):
        md = """This is a paragraph.
    This continues the paragraph.

Another paragraph."""
        expected = [
            "This is a paragraph.\nThis continues the paragraph.",
            "Another paragraph."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_unordered_list(self):
        md = """- Item one
- Item two

- Item three"""
        expected = [
            "- Item one\n- Item two",
            "- Item three"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_ordered_list(self):
        md = """1. First item
2. Second item

3. Third item"""
        expected = [
            "1. First item\n2. Second item",
            "3. Third item"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_whitespace_only(self):
        md = "   \n \n\t"
        self.assertEqual(markdown_to_blocks(md), [])

if __name__ == "__main__":
    unittest.main()