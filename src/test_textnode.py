import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("Same", TextType.IMAGE)
        node2 = TextNode("Sure?", TextType.IMAGE)
        self.assertNotEqual(node, node2)

        node = TextNode("Same", TextType.LINK, url=None)
        node2 = TextNode("Same", TextType.LINK)
        self.assertEqual(node, node2)

        node = TextNode("Same type", TextType.LINK)
        node2 = TextNode("Sure?", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.net.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), '<a href="www.net.com">This is a text node</a>')

    def test_text_img(self):
        node = TextNode("This is a text node", TextType.IMAGE, "www.img.net")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="www.img.net" alt="This is a text node"></img>')

if __name__ == "__main__":
    unittest.main()
