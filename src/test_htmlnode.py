import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Create an HTMLNode with specific props
        node = HTMLNode("p", "This is a paragraph", [], {"class": "text"})
        node2 = HTMLNode("p", "This is a paragraph", [], {"class": "text"})
        node3 = HTMLNode("p", "This is a paragraph", [], {"class": "text", "id": "unique"})
        
        result = node.props_to_html()
        result2 = node2.props_to_html()
        result3 = node3.props_to_html()
        
        
        
        self.assertEqual(result, result2)
        self.assertNotEqual(result, result3)
        

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("ul", "Hello, world!")
        node3 = LeafNode("p", "Hello, world!", {"class": "text"})
        node4 = LeafNode("p", None, {"class": "text"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<ul>Hello, world!</ul>")
        self.assertEqual(node3.to_html(), "<p class=\"text\">Hello, world!</p>")
        with self.assertRaises(ValueError):
            node4.to_html()


    def test_to_html_with_children(self):
        # Create a ParentNode with children
        child1 = LeafNode("span", "Child 1")
        child2 = LeafNode("span", "Child 2")
        parent = ParentNode("div", [child1, child2], {"class": "parent"})
        
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
        empty_parent = ParentNode("div", [])
        self.assertEqual(empty_parent.to_html(), "<div></div>")

        expected_html = '<div class="parent"><span>Child 1</span><span>Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

        nested = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("p", "deep content")
                ])
            ])
        ])
        self.assertEqual(nested.to_html(), "<div><section><article><p>deep content</p></article></section></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )

    def test_text(self):
        # Testing NORMAL text type
        node_normal = TextNode("This is normal text", TextType.NORMAL)
        html_node_normal = text_node_to_html_node(node_normal)
        self.assertEqual(html_node_normal.tag, None)
        self.assertEqual(html_node_normal.value, "This is normal text")

        # Testing BOLD text type
        node_bold = TextNode("This is bold text", TextType.BOLD)
        html_node_bold = text_node_to_html_node(node_bold)
        self.assertEqual(html_node_bold.tag, "b")
        self.assertEqual(html_node_bold.value, "This is bold text")

        # Testing ITALIC text type
        node_italic = TextNode("This is italic text", TextType.ITALIC)
        html_node_italic = text_node_to_html_node(node_italic)
        self.assertEqual(html_node_italic.tag, "i")
        self.assertEqual(html_node_italic.value, "This is italic text")

        # Testing CODE text type
        node_code = TextNode("This is code text", TextType.CODE)
        html_node_code = text_node_to_html_node(node_code)
        self.assertEqual(html_node_code.tag, "code")
        self.assertEqual(html_node_code.value, "This is code text")

        # Testing LINK text type
        node_link = TextNode("This is a link", TextType.LINK, "http://example.com")
        html_node_link = text_node_to_html_node(node_link)
        self.assertEqual(html_node_link.tag, "a")
        self.assertEqual(html_node_link.value, "This is a link")
        self.assertEqual(html_node_link.props, {"href": "http://example.com"})

        # Testing IMAGE text type
        node_image = TextNode("This is an image", TextType.IMAGE, "http://example.com/image.jpg")
        html_node_image = text_node_to_html_node(node_image)
        self.assertEqual(html_node_image.tag, "img")
        self.assertEqual(html_node_image.props, {"src": "http://example.com/image.jpg", "alt": "This is an image"})


if __name__ == "__main__":
    unittest.main()

    