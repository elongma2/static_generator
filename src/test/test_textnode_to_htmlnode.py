from textnode import TextNodeType,TextNode 
from htmlnode import LeafNode
import unittest

def text_node_to_html_node(text_node):
   if text_node.type not in [TextNodeType.NORMAL_TEXT, TextNodeType.BOLD_TEXT, TextNodeType._ITALIC_TEXT, TextNodeType.CODE_TEXT, TextNodeType.LINK, TextNodeType.IMAGE]:
       raise Exception("Invalid text node type")
   if text_node.type == TextNodeType.NORMAL_TEXT:
       return LeafNode(value = text_node.text)
   elif text_node.type == TextNodeType.BOLD_TEXT:
       return LeafNode("b", text_node.text)
   elif text_node.type == TextNodeType._ITALIC_TEXT:
       return LeafNode("i", text_node.text)
   elif text_node.type == TextNodeType.CODE_TEXT:
       return LeafNode("code", text_node.text)
   elif text_node.type == TextNodeType.LINK:
       return LeafNode("a", text_node.text, {"href": text_node.url})
   elif text_node.type == TextNodeType.IMAGE:
       return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
   

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextNodeType.NORMAL_TEXT )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_bold(self):
        node = TextNode("This is a text node", TextNodeType.BOLD_TEXT )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_link(self):
        node = TextNode("This is a text node", TextNodeType.LINK, "https://www.google.com" )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})