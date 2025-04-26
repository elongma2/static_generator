import unittest
from textnode import TextNode, TextNodeType
from helper_func import extract_markdown_images,split_nodes_link

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.type != TextNodeType.NORMAL_TEXT:
            new_nodes.append(node)
            continue

        extracted_images = extract_markdown_images(node.text)

        #counter 
        idx = 0
        for alt,image in extracted_images:
            image_syntax = f"![{alt}]({image})"
            match_start = node.text.find(image_syntax)

            if match_start == -1:
                continue
            
            #add text before image
            if match_start > idx:
                new_nodes.append(TextNode(node.text[idx:match_start], TextNodeType.NORMAL_TEXT))
            
            #add image
            new_nodes.append(TextNode(alt, TextNodeType.IMAGE, image))
            idx = match_start + len(image_syntax)

        #add text after image
        if idx < len(node.text):
            remaining = node.text[idx:]
            new_nodes.append(TextNode(remaining, TextNodeType.NORMAL_TEXT))

    return new_nodes

node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextNodeType.NORMAL_TEXT,
        )



class TestImageSplitter(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextNodeType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextNodeType.NORMAL_TEXT),
                TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextNodeType.NORMAL_TEXT),
                TextNode(
                    "second image", TextNodeType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        ) 

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com)",
            TextNodeType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.NORMAL_TEXT),
                TextNode("link", TextNodeType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_link_multiple(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [youtube](https://www.youtube.com)",
            TextNodeType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNodeType.NORMAL_TEXT),
                TextNode("link", TextNodeType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextNodeType.NORMAL_TEXT),
                TextNode("youtube", TextNodeType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )