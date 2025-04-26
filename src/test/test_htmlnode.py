import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):        
        node = HTMLNode("div", "Hello")
        node2 = HTMLNode("div", "Hello")
        self.assertEqual(vars(node), vars(node2))
    
    def test_repr(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(str(node), "HTMLNode(tag=p, value=Hello, props=None, children=None)")
    
    def test_props_to_html(self):
        node = HTMLNode("p", "Hello", props={"class": "test", "id": "test"})
        self.assertEqual(node.props_to_html() , 'class="test" id="test"')