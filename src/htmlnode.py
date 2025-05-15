

class HTMLNode(object):
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        return "".join(f' {key}="{value}"' for key, value in sorted(self.props.items()))
        
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" 

class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        super().__init__(tag=tag, children=children if children is not None else [], props=props)

    def add_child(self, child):
        self.children.append(child)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            print("Warning: ParentNode has no children")

        children_html = ""
        for child in self.children:
            if hasattr(child, 'to_html'):
                children_html += child.to_html()
            elif hasattr(child, 'text'):
                children_html += child.text
            else:
                children_html += str(child)

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
