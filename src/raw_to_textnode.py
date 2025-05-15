import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            # Handle unmatched delimiter gracefully
            new_nodes.append(node)  # Add the entire node as is
            continue
        
        for i, part in enumerate(parts):
            # Alternate between NORMAL and the new text_type
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.NORMAL))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    return (re.findall("!\[([^\[\]]*)\]\(([^\(\)]*)\)", text))
    
def extract_markdown_links(text):
    return (re.findall("(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text))

def split_nodes_images(old_nodes):
    new_nodes = []
    image_pattern = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        pos = 0
        for match in image_pattern.finditer(node.text):
            start, end = match.span()
            alt_text, url = match.groups()
            
            # Text before the match
            if start > pos:
                new_nodes.append(TextNode(node.text[pos:start], TextType.NORMAL))
            
            # The image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            pos = end
        
        # Remaining text after last match
        if pos < len(node.text):
            new_nodes.append(TextNode(node.text[pos:], TextType.NORMAL))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    link_pattern = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        pos = 0
        for match in link_pattern.finditer(node.text):
            start, end = match.span()
            text, url = match.groups()

            if start > pos:
                new_nodes.append(TextNode(node.text[pos:start], TextType.NORMAL))

            new_nodes.append(TextNode(text, TextType.LINK, url))
            pos = end

        if pos < len(node.text):
            new_nodes.append(TextNode(node.text[pos:], TextType.NORMAL))

    return new_nodes




def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Recursively convert markdown text into a list of TextNodes.
    Handles nested formatting: bold, italic, code, links, and images.
    """
    nodes = [TextNode(text, TextType.NORMAL)]
    
    # First handle images and links (they take priority and shouldn't be nested)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)

    # Then handle inline code, bold, italic recursively
    nodes = recursively_format_nodes(nodes)

    return nodes

def recursively_format_nodes(nodes: list[TextNode]) -> list[TextNode]:
    formatted_nodes = []

    for node in nodes:
        if node.text_type != TextType.NORMAL:
            formatted_nodes.append(node)
            continue

        text = node.text

        # Order matters: code > bold > italic
        match = re.search(r"`(.*?)`", text)
        if match:
            formatted_nodes.extend(
                recursively_format_nodes_from_match(text, match, TextType.CODE, "`")
            )
            continue

        match = re.search(r"\*\*(.*?)\*\*", text)
        if match:
            formatted_nodes.extend(
                recursively_format_nodes_from_match(text, match, TextType.BOLD, "**")
            )
            continue

        match = re.search(r"_(.*?)_", text)
        if match:
            formatted_nodes.extend(
                recursively_format_nodes_from_match(text, match, TextType.ITALIC, "_")
            )
            continue

        # No formatting found
        formatted_nodes.append(TextNode(text, TextType.NORMAL))

    return formatted_nodes

def recursively_format_nodes_from_match(text, match, text_type, delimiter):
    before = text[:match.start()]
    matched_text = match.group(1)
    after = text[match.end():]

    nodes = []

    if before:
        nodes.extend(recursively_format_nodes([TextNode(before, TextType.NORMAL)]))

    # Recurse inside matched_text
    inner_nodes = recursively_format_nodes([TextNode(matched_text, TextType.NORMAL)])
    if len(inner_nodes) == 1:
        # Wrap with the current text_type
        inner_nodes[0].text_type = text_type
        nodes.append(inner_nodes[0])
    else:
        # If it's multiple nodes, we join them back as plain text under current format
        joined = ''.join(n.text for n in inner_nodes)
        nodes.append(TextNode(joined, text_type))

    if after:
        nodes.extend(recursively_format_nodes([TextNode(after, TextType.NORMAL)]))

    return nodes


