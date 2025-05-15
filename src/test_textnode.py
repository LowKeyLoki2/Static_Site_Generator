import unittest
from textnode import TextNode, TextType




class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        node3 = TextNode("this is not a text node", TextType.BOLD, None)
        node4 = TextNode("This is a text node", TextType.NORMAL, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)

    

if __name__ == "__main__":
    unittest.main()