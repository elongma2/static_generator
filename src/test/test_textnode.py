import unittest
from textnode import TextNode, TextNodeType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextNodeType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextNodeType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextNodeType.BOLD_TEXT)
        self.assertEqual(str(node), "TextNode(text='This is a text node', type=1, url=None)")
    
    def test_nq(self):
        node = TextNode("This is another text node", TextNodeType.BOLD_TEXT)
        node2 = TextNode("This is another text node", TextNodeType.IMAGE)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()