class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Not implemented yet!")
    
    def props_to_html(self):
        if self.props:
            result = ""
            for prop in self.props:
                result += f'{prop}="{self.props[prop]}" '
            return result
        return ""
    
    def __repr__(self):
        return f"tag: {self.tag} value: {self.value} children: {self.children} props: {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value
        if self.props_to_html() == "":
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"tag: {self.tag} value: {self.value} props: {self.props}"
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.children is None:
            raise ValueError("Parent node must have children")
        if self.tag is None:
            raise ValueError("Parent node must have tag")
        return self.props_to_html() + f"<{self.tag}>" + "".join([child.to_html() for child in self.children]) + f"</{self.tag}>"
    