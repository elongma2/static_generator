import unittest
from textnode import TextNode, TextNodeType
from helper_func import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "Hello **world**"
        expected_nodes = [
            TextNode("Hello ", TextNodeType.NORMAL_TEXT),
            TextNode("world", TextNodeType.BOLD_TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected_nodes)

    def test_text_to_textnodes_with_links(self):
        text = "Hello [world](https://example.com) **world** bruh"
        expected_nodes = [
            TextNode("Hello ", TextNodeType.NORMAL_TEXT),
            TextNode("world", TextNodeType.LINK, "https://example.com"),
            TextNode(" ", TextNodeType.NORMAL_TEXT),
            TextNode("world", TextNodeType.BOLD_TEXT),
            TextNode(" bruh", TextNodeType.NORMAL_TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected_nodes)

    def test_with_all_types(self):
        text = "Hello [world](https://example.com) **world** bruh ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected_nodes = [
            TextNode("Hello ", TextNodeType.NORMAL_TEXT),
            TextNode("world", TextNodeType.LINK, "https://example.com"),
            TextNode(" ", TextNodeType.NORMAL_TEXT),
            TextNode("world", TextNodeType.BOLD_TEXT),
            TextNode(" bruh ", TextNodeType.NORMAL_TEXT),
            TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(text_to_textnodes(text), expected_nodes)
