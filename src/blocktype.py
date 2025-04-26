from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    lines = markdown.split("\n")

    # Code block
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    
    # Heading
    if lines[0].startswith("#") and lines[0].lstrip("#").startswith(" "):
        numhash = len(lines[0]) - len(lines[0].lstrip("#"))
        if numhash <= 6:
            return BlockType.HEADING
        
    # Quote block
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    # Unordered list
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
        
    # Ordered list
    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def is_ordered_list(lines):
    for i, line in enumerate(lines):
        if ". " not in line:
            return False
        
        number = line.split(". ")[0]
        if not number.isdigit():
            return False
        
        if i+1 != int(number):
            return False
        
    return True
