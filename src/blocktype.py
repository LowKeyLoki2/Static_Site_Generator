from enum import Enum
import re

class BlockType(Enum):
    """Enum for block types in a document."""
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
   

def block_to_block_type(block):
    """
    Convert a block to its corresponding BlockType.

    If the block does not match any specific type, it defaults to BlockType.PARAGRAPH.
    """
    lines = block.strip().splitlines()
    if block.lstrip().startswith("#") and block.lstrip().split(" ", 1)[0].count("#") > 0:
        return BlockType.HEADING
    elif block.startswith("> "):
        return BlockType.QUOTE
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\.\s", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH