import unittest
import re
from textnode import TextNode, TextType
from raw_to_textnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes
from markdown_to_blocks import markdown_to_blocks
from blocktype import BlockType, block_to_block_type
from markdown_to_blocks import *
from htmlnode import ParentNode

def text_to_textnodes(text):
    nodes = []
    patterns = [
        (r'\*\*(.*?)\*\*', TextType.BOLD),
        (r'\*(.*?)\*', TextType.ITALIC),
        (r'`(.*?)`', TextType.CODE),
        (r'!\[(.*?)\]\((.*?)\)', TextType.IMAGE),
        (r'\[(.*?)\]\((.*?)\)', TextType.LINK),
    ]

    while text:
        match = None
        for pattern, text_type in patterns:
            match = re.search(pattern, text)
            if match:
                break

        if not match:
            nodes.append(TextNode(text, TextType.NORMAL))
            break

        start, end = match.span()
        if start > 0:
            nodes.append(TextNode(text[:start], TextType.NORMAL))

        if text_type in {TextType.IMAGE, TextType.LINK}:
            nodes.append(TextNode(match.group(1), text_type, match.group(2)))
        else:
            nodes.append(TextNode(match.group(1), text_type))

        text = text[end:]

    return nodes
       

class TestHTMLNode(unittest.TestCase):
        
    def test_empty_node(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)


    def test_no_delimiter(self):
        node = TextNode("This is text without a delimiter", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text without a delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
    
    def test_single_delimiter(self):
        node = TextNode("This is `code` text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
        
    def test_multiple_delimiters(self):
        node = TextNode("Here is `code1` and `code2` too", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Here is ")
        self.assertEqual(new_nodes[1].text, "code1")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "code2")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " too")

    def test_unmatched_delimiter(self):
        node = TextNode("This is `broken code", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    
    def test_non_normal_node(self):
        node = TextNode("This is already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)
        
    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png)"
        expected = [("alt text", "http://example.com/image.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_multiple_markdown_images(self):
        text = "![img1](url1) some text ![img2](url2)"
        expected = [("img1", "url1"), ("img2", "url2")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        text = "This is a [link](http://example.com)"
        expected = [("link", "http://example.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_excludes_images(self):
        text = "This is a [link](http://example.com) and ![img](img.png)"
        expected = [("link", "http://example.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_multiple_links(self):
        text = "[one](url1) and [two](url2)"
        expected = [("one", "url1"), ("two", "url2")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)


    def test_split_nodes_images_basic(self):
        input_nodes = [TextNode("This is an image ![alt](img.png)", TextType.NORMAL)]
        result = split_nodes_images(input_nodes)
        expected = [
            TextNode("This is an image ", TextType.NORMAL),
            TextNode("alt", TextType.IMAGE, "img.png"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_images_multiple(self):
        input_nodes = [TextNode("![a](1.png) and ![b](2.png)", TextType.NORMAL)]
        result = split_nodes_images(input_nodes)
        expected = [
            TextNode("a", TextType.IMAGE, "1.png"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("b", TextType.IMAGE, "2.png"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_images_with_trailing_text(self):
        input_nodes = [TextNode("Image: ![alt](img.png) done", TextType.NORMAL)]
        result = split_nodes_images(input_nodes)
        expected = [
            TextNode("Image: ", TextType.NORMAL),
            TextNode("alt", TextType.IMAGE, "img.png"),
            TextNode(" done", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_links_basic(self):
        input_nodes = [TextNode("Visit [Google](https://google.com)", TextType.NORMAL)]
        result = split_nodes_links(input_nodes)
        expected = [
            TextNode("Visit ", TextType.NORMAL),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_links_exclude_images(self):
        input_nodes = [TextNode("Image ![alt](img.png) and [link](url)", TextType.NORMAL)]
        result = split_nodes_links(input_nodes)
        expected = [
            TextNode("Image ![alt](img.png) and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(result, expected)

    def test_non_normal_nodes_are_untouched(self):
        input_nodes = [TextNode("![alt](img.png)", TextType.IMAGE)]
        result_images = split_nodes_images(input_nodes)
        result_links = split_nodes_links(input_nodes)
        self.assertEqual(result_images, input_nodes)
        self.assertEqual(result_links, input_nodes)

    def test_split_nodes_links_multiple(self):
        input_nodes = [TextNode("[one](url1) and [two](url2)", TextType.NORMAL)]
        result = split_nodes_links(input_nodes)
        expected = [
            TextNode("one", TextType.LINK, "url1"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("two", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_basic_text(self):
        text = "This is a simple text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a simple text.", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text = "This is *italic* text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        text = "This is `inline code` text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("inline code", TextType.CODE),
            TextNode(" text.", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_link_text(self):
        text = "This is a [link](http://example.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_image_text(self):
        text = "This is an image ![alt text](http://example.com/image.jpg)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an image ", TextType.NORMAL),
            TextNode("alt text", TextType.IMAGE, "http://example.com/image.jpg"),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_multiple_markdown(self):
        text = "This is **bold**, *italic*, `inline code`, and a [link](http://example.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.NORMAL),
            TextNode("inline code", TextType.CODE),
            TextNode(", and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_image_and_link(self):
        text = "Here is an image ![alt](http://example.com/image.png) and a [link](http://example.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is an image ", TextType.NORMAL),
            TextNode("alt", TextType.IMAGE, "http://example.com/image.png"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        text = "This is a `broken code"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a `broken code", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text = ""
        result = text_to_textnodes(text)
        expected = []
        self.assertEqual(result, expected)

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
            ],
        )  
    
    def test_markdown_to_block(self):
        markdown = """# Header 1

    This is a paragraph.

    # Header 2

    Another paragraph."""
        
        expected = [
            "# Header 1",
            "This is a paragraph.",
            "# Header 2",
            "Another paragraph."
        ]
        
        result = markdown_to_blocks(markdown)
        assert result == expected, f"Expected {expected}, but got {result}"



    def test_single_paragraph(self):
        md = "This is a simple paragraph with no breaks."
        expected = ["This is a simple paragraph with no breaks."]
        self.assertEqual(markdown_to_blocks(md), expected)

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

    def test_list_items(self):
        md = """- Item one
- Item two

- Item three"""
        expected = [
            "- Item one\n- Item two",
            "- Item three"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_empty_string(self):
        md = ""
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_whitespace_only(self):
        md = "   \n \n\t"
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)


    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("   ### Indented heading"), BlockType.HEADING)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_fake_code_block(self):
        self.assertEqual(block_to_block_type("```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```python"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Another list item"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("9. Ninth item"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("   Just some indented text."), BlockType.PARAGRAPH)

    def test_edge_cases(self):
        self.assertEqual(block_to_block_type("1) Not a list"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Random text with > symbol"), BlockType.PARAGRAPH)

    def test_valid_code_block(self):
        block = "```\ndef foo():\n    return 42\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_valid_code_block_with_language(self):
        block = "```python\ndef foo():\n    return 42\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_unclosed_code_block(self):
        block = "```python\ndef foo():\n    return 42"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_only_opening_triple_backticks(self):
        block = "```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_only_closing_triple_backticks(self):
        block = "def foo():\n    return 42\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_inline_code_is_not_block(self):
        block = "This is some `inline code` in a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_regular_paragraph(self):
        paragraph = "Just a regular paragraph with no backticks."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)

    def test_textnode_repr(self):
        node = TextNode("Hello", TextType.NORMAL)
        self.assertEqual(repr(node), "TextNode(Hello, normal, None)")
        
        node_with_url = TextNode("Click me", TextType.LINK, "https://example.com")
        self.assertEqual(repr(node_with_url), "TextNode(Click me, link, https://example.com)")


    def test_empty_markdown(self):
        """Test that an empty Markdown string returns an empty <div>."""
        markdown = ""
        node = markdown_to_html_node(markdown)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.to_html(), "<div></div>")

    

    def test_heading_conversion(self):
        block = "# Heading Text"
        node = create_heading_node(block)
        self.assertEqual(node.tag, "h1")
        self.assertIn("Heading Text", node.to_html())

    def test_paragraph_conversion(self):
        block = "This is a paragraph."
        node = create_paragraph_node(block)
        self.assertEqual(node.tag, "p")
        self.assertIn("This is a paragraph.", node.to_html())

    def test_code_block_conversion(self):
        block = "```\ndef foo():\n    return 'bar'\n```"
        node = create_code_node(block)
        self.assertEqual(node.tag, "pre")
        self.assertEqual(node.children[0].tag, "code")
        self.assertIn("def foo()", node.to_html())

    def test_quote_block_conversion(self):
        block = "> This is a quote\n> with two lines"
        node = create_quote_node(block)
        self.assertEqual(node.tag, "blockquote")
        self.assertIn("This is a quote with two lines", node.to_html())

    def test_unordered_list_conversion(self):
        block = "- Item one\n- Item two"
        node = create_unordered_list_node(block)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 2)
        self.assertIn("<li>Item one</li>", node.to_html())

    def test_ordered_list_conversion(self):
        block = "1. First item\n2. Second item"
        node = create_ordered_list_node(block)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 2)
        self.assertIn("<li>First item</li>", node.to_html())

    def test_full_markdown_conversion(self):
        md = "# Title\n\nParagraph here.\n\n- List item 1\n- List item 2"
        html_node = markdown_to_html_node(md)
        html = html_node.to_html()
        self.assertIn("<h1>", html)
        self.assertIn("<p>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<li>List item 1</li>", html)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

   
    

if __name__ == '__main__':
    unittest.main()
