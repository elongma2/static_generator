import unittest
from textnode import TextNode, TextNodeType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.type != TextNodeType.NORMAL_TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextNodeType.NORMAL_TEXT))
            else:
                new_nodes.append(TextNode(part, text_type)) 

    return new_nodes

class TestSplitDelimeter(unittest.TestCase):
    def test_split_delimeter_code(self):
        node = TextNode("This is a text with a `code block` word", TextNodeType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextNodeType.CODE_TEXT)
        self.assertEqual(
            [
                TextNode("This is a text with a ", TextNodeType.NORMAL_TEXT),
                TextNode("code block", TextNodeType.CODE_TEXT),
                TextNode(" word", TextNodeType.NORMAL_TEXT),
            ],
            new_nodes
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextNodeType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextNodeType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.NORMAL_TEXT),
                TextNode("bolded", TextNodeType.BOLD_TEXT),
                TextNode(" word", TextNodeType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_multiple(self):
        node = TextNode("This is **text** with a **bolded** word", TextNodeType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextNodeType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is ", TextNodeType.NORMAL_TEXT),
                TextNode("text", TextNodeType.BOLD_TEXT),
                TextNode(" with a ", TextNodeType.NORMAL_TEXT),
                TextNode("bolded", TextNodeType.BOLD_TEXT),
                TextNode(" word", TextNodeType.NORMAL_TEXT),
            ],
            new_nodes,
        )

        


        


    