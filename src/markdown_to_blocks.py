from blocktype import block_to_block_type, BlockType
from htmlnode import ParentNode, LeafNode
from raw_to_textnode import text_to_textnodes
from textnode import text_node_to_html_node
import re

def markdown_to_blocks(markdown: str) -> list:
    """
    Convert markdown text to a list of blocks.
    """
    lines = markdown.split('\n')
    blocks = []
    current_block = []

    for line in lines:
        if not line.strip():
            if current_block:
                blocks.append('\n'.join(line.strip() for line in current_block))
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append('\n'.join(line.strip() for line in current_block))

    return blocks

def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Convert markdown text into an HTML node tree.
    """
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode("div", children=[])

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            parent.add_child(create_heading_node(block))
        elif block_type == BlockType.PARAGRAPH:
            parent.add_child(create_paragraph_node(block))
        elif block_type == BlockType.CODE:
            parent.add_child(create_code_node(block))
        elif block_type == BlockType.QUOTE:
            parent.add_child(create_quote_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            parent.add_child(create_unordered_list_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            parent.add_child(create_ordered_list_node(block))
        else:
            # Fallback to paragraph
            parent.add_child(create_paragraph_node(block))

    return parent

def create_paragraph_node(block: str) -> ParentNode:
    text_nodes = text_to_textnodes(block.replace("\n", " "))
    html_nodes = [text_node_to_html_node(n) for n in text_nodes]
    return ParentNode(tag="p", children=html_nodes)

def create_heading_node(block: str) -> ParentNode:
    stripped = block.lstrip()
    level = min(stripped.count("#"), 6)  # Clamp to h6 max
    content = stripped[level:].strip()
    text_nodes = text_to_textnodes(content)
    html_nodes = [text_node_to_html_node(n) for n in text_nodes]
    return ParentNode(tag=f"h{level}", children=html_nodes)

def create_quote_node(block: str) -> ParentNode:
    quote_lines = [line.lstrip("> ").strip() for line in block.splitlines()]
    content = " ".join(quote_lines)
    text_nodes = text_to_textnodes(content)
    html_nodes = [text_node_to_html_node(n) for n in text_nodes]
    return ParentNode(tag="blockquote", children=html_nodes)

def create_code_node(block: str) -> ParentNode:
    lines = block.splitlines()
    code_content = "\n".join(lines[1:-1] if lines[0].startswith("```") else lines)
    return ParentNode(tag="pre", children=[LeafNode(tag="code", value=code_content)])

def create_unordered_list_node(block: str) -> ParentNode:
    items = [line.lstrip("- ").strip() for line in block.splitlines()]
    list_items = [
        ParentNode(tag="li", children=[text_node_to_html_node(n) for n in text_to_textnodes(item)])
        for item in items if item
    ]
    return ParentNode(tag="ul", children=list_items)

def create_ordered_list_node(block: str) -> ParentNode:
    items = [re.sub(r"^\d+\.\s*", "", line).strip() for line in block.splitlines()]
    list_items = [
        ParentNode(tag="li", children=[text_node_to_html_node(n) for n in text_to_textnodes(item)])
        for item in items if item
    ]
    return ParentNode(tag="ol", children=list_items)
