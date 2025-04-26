import unittest
from htmlnode import ParentNode,LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode([child_node], "div",)
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode( [grandchild_node], "span",)
        parent_node = ParentNode( [child_node], "div",)
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode([child_node], "div", props={"class": "test"})
        self.assertEqual(parent_node.to_html(), '<div class="test"><span>child</span></div>')