class HTMLNode:
    def __init__(self, tag = None , value = None ,  props = None, children = None ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return ' '.join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props}, children={self.children})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        elif self.tag is None:
            return self.value
        else:
            if self.props is None:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, children , tag , props=None ):
        super().__init__(tag=tag,  props=props, children=children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode tag cannot be None")
        
        if self.children is None:
            raise ValueError("ParentNode children cannot be None")
        
        innerjoint = "".join(child.to_html() for child in self.children)

        if self.props is None:
            return f"<{self.tag}>{innerjoint}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{innerjoint}</{self.tag}>"

        

        
        




        