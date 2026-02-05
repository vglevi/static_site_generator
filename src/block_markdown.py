from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def markdown_to_blocks(markdown: str) -> list[str]:
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block != "":
            result.append(block)
    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"

def block_to_block_type(block: str) -> BlockType:
    block_lines = block.splitlines(keepends=True)

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(block_lines) > 1 and block_lines[0].startswith("```") and block_lines[-1].startswith("```"):
        return BlockType.CODE

    if len(block_lines) == len([1 for line in block_lines if line.startswith(">")]):
        return BlockType.QUOTE

    if len(block_lines) == len([1 for line in block_lines if line.startswith("- ")]):
        return BlockType.ULIST

    if len(block_lines) == len([1 for i, line in enumerate(block_lines, 1) if line.startswith(f"{i}. ")]):
        return BlockType.OLIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def block_to_html_node(block: str):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)

def text_to_children(text: str):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.splitlines()
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
        if level + 1 >= len(block):
            raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block: str) -> ParentNode:
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.splitlines()
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block: str) -> ParentNode:
    items = block.splitlines()
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block: str) -> ParentNode:
    lines = block.splitlines()
    text = ""
    for line in lines:
        text += " " + line[1:].lstrip()
    children = text_to_children(text.lstrip())
    return ParentNode("blockquote", children)

def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("#").strip()
    raise Exception("Can't find h1 header")
