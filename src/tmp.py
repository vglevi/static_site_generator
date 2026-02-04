from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType

node = TextNode("This is text with a `code block` word", TextType.TEXT)
node2 = TextNode("And this is text with a `code block` word", TextType.TEXT)
print(split_nodes_delimiter([node, node2], "`", TextType.CODE))
