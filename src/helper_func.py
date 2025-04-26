from textnode import TextNodeType,TextNode 
from htmlnode import LeafNode,HTMLNode,ParentNode
from blocktype import block_to_block_type, BlockType
import re
import os
from pathlib import Path
def text_node_to_html_node(text_node):
   if text_node.type not in [
    TextNodeType.NORMAL_TEXT,
    TextNodeType.BOLD_TEXT,
    TextNodeType._ITALIC_TEXT,
    TextNodeType.CODE_TEXT,
    TextNodeType.LINK,
    TextNodeType.IMAGE,
]:
    raise Exception("Invalid text node type")
   if text_node.type == TextNodeType.NORMAL_TEXT:
       return LeafNode(value = text_node.text)
   elif text_node.type == TextNodeType.BOLD_TEXT:
       return LeafNode(tag = "b", value=text_node.text)
   elif text_node.type == TextNodeType._ITALIC_TEXT:
       return LeafNode(tag = "i", value = text_node.text)
   elif text_node.type == TextNodeType.CODE_TEXT:
       return LeafNode(tag = "code", value = text_node.text)
   elif text_node.type == TextNodeType.LINK:
       return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
   elif text_node.type == TextNodeType.IMAGE:
       return LeafNode(tag = "img", value="", props={"src": text_node.url, "alt": text_node.text})
   
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

def extract_markdown_images(text):
    pattern = r"!\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

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

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.type != TextNodeType.NORMAL_TEXT:
            new_nodes.append(node)
            continue

        extracted_links = extract_markdown_links(node.text)

        #counter 
        idx = 0
        for text,url in extracted_links:
            link_syntax = f"[{text}]({url})"
            match_start = node.text.find(link_syntax)

            if match_start == -1:
                continue
            
            #add text before image
            if match_start > idx:
                new_nodes.append(TextNode(node.text[idx:match_start], TextNodeType.NORMAL_TEXT))
            
            #add image
            new_nodes.append(TextNode(text, TextNodeType.LINK, url))
            idx = match_start + len(link_syntax)

        #add text after image        
        if idx < len(node.text):
            remaining = node.text[idx:]
            new_nodes.append(TextNode(remaining, TextNodeType.NORMAL_TEXT))

    return new_nodes

def text_to_textnodes(text):

    new_nodes = [TextNode(text, TextNodeType.NORMAL_TEXT)]

    # 1. Code
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextNodeType.CODE_TEXT)

    # 2. Bold
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextNodeType.BOLD_TEXT)

    # 3. Italic
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextNodeType._ITALIC_TEXT)

    # ✅ 4. Images must come before links!
    new_nodes = split_nodes_image(new_nodes)

    # ✅ 5. Then handle links
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes

def markdown_to_blocks(markdown):
    markdown = markdown.split("\n\n")
    clean_blocks = []
    for block in markdown:
        lines = block.strip().split("\n")
        strpped_lines = [line.strip() for line in lines]
        clean_block = "\n".join(strpped_lines)
        clean_blocks.append(clean_block)
        
    return clean_blocks

def markdown_to_html_nodes(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)
    return ParentNode(children = children, tag ="div")




def text_to_children(text):
    nodes = text_to_textnodes(text)
    children =[]
    for node in nodes:
        leaf_node = text_node_to_html_node(node)
        children.append(leaf_node)
    return children


def block_to_html_node(block, block_type):
    if block_type == BlockType.HEADING:
        num_hashes = len(block.split(" ")[0])
        content = block[num_hashes+1:]
        return ParentNode(tag=f"h{num_hashes}", children= text_to_children(content))
    
    elif block_type == BlockType.PARAGRAPH:
        line = block.split("\n")
        content = " ".join(line)
        return ParentNode(tag="p", children= text_to_children(content))
    
    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode(tag="blockquote", children=children)
    
    elif block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        items = []

        for line in lines:
            if not line.startswith("- "):
                raise ValueError("invalid unordered list block")
            text = line[2:]
            children = text_to_children(text)
            items.append(ParentNode(tag="li", children=children))
        return ParentNode(tag="ul", children=items)
    
    elif block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        items = []

        for i, line in enumerate(lines):
            expected_prefix = f"{i + 1}. "
            if not line.startswith(expected_prefix):
                raise ValueError("invalid ordered list block")
            text = line[len(expected_prefix):]
            children = text_to_children(text)
            items.append(ParentNode(tag="li", children=children))
        return ParentNode(tag="ol", children=items)
    
    elif block_type == BlockType.CODE:
        if not block.startswith("```") or not block.endswith("```"):
            raise ValueError("invalid code block")
        text = block[4:-3]
        #node = TextNode(text, TextNodeType.CODE_TEXT)
        code = LeafNode(tag= "code", value = text if text else "")   # just 1 <code>
        return ParentNode(tag="pre", children=[code])
  
def extract_title(markdown):
    
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 header found")

def generate_page(from_path,template_path,dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")

    #read markdown and template files
    from_path_content = open(from_path).read()
    template_path_content = open(template_path).read()


    markdown_nodes = markdown_to_html_nodes(from_path_content).to_html()

    #extract title
    title = extract_title(from_path_content)

    #replace content and title headings
    template_path_content = template_path_content.replace("{{ Title }}", title)
    template_path_content = template_path_content.replace("{{ Content }}", markdown_nodes)
    
    # Write output
    with open(dest_path, "w") as f:
        f.write(template_path_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
            
    
            

