from enum import Enum

class TextNodeType(Enum):
    NORMAL_TEXT = 0
    BOLD_TEXT = 1
    _ITALIC_TEXT = 2
    CODE_TEXT = 3
    LINK = 4
    IMAGE = 5

class TextNode:
    def __init__(self, text, Text_type, url = None):
        
        self.text = text
        self.type = Text_type
        self.url = url
        
    def __eq__(self, value):
        return (self.text == value.text and self.type == value.type and self.url == value.url)
    def __repr__(self):
        return f"TextNode(text='{self.text}', type={self.type.value}, url={self.url})"
    
    
    
