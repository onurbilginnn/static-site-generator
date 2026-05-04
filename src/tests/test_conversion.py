import unittest

from textnode.textnode import TextNode, TextType
from textnode.utils import text_node_to_html_node,\
                  split_nodes_delimiter,\
                  extract_markdown_images,\
                  extract_markdown_links,\
                  split_nodes_link,\
                  split_nodes_image,\
                  text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        node2 = TextNode("This is a image node", TextType.IMAGE, "example.com")
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "img")
        self.assertEqual(html_node2.props["alt"], "This is a image node")
        self.assertEqual(html_node2.props["src"], "example.com")
        node3 = TextNode("This is a link node", TextType.LINK, "example.com")
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node3.tag, "a")
        self.assertEqual(html_node3.props["href"], "example.com")
        self.assertEqual(html_node3.value, "This is a link node")
    
    def test_text_to_textnode(self):
        node = TextNode("This is text `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("This is text ", TextType.TEXT))
        node2 = TextNode("This is text `code block word``", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node2], "`", TextType.CODE)
        self.assertEqual(context.exception.args[0],
                         "Invalid markdown syntax!")

    def test_extract_markdown_images(self):
        image_test1 = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_test1)
        link_test1 = extract_markdown_links("This is a test [Google](https://www.google.com) and another [GitHub](https://www.github.com)")
        self.assertListEqual([("Google", "https://www.google.com"), ("GitHub", "https://www.github.com")], link_test1)

    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) or [to github](https://www.github.com)",
        TextType.TEXT,
        )
        node2 = TextNode(
        "This is 2ns text with a link [to hiyar](https://www.hiyar.dev) and [to got](https://www.got.com/) END",
        TextType.TEXT,
        )
        self.assertEqual(split_nodes_link([node, node2]), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" or ", TextType.TEXT),
            TextNode("to github", TextType.LINK, "https://www.github.com"),
            TextNode("This is 2ns text with a link ", TextType.TEXT),
            TextNode("to hiyar", TextType.LINK, "https://www.hiyar.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to got", TextType.LINK, "https://www.got.com/"),
            TextNode(" END", TextType.TEXT)
        ])
    
    def test_split_nodes_image(self):
        node = TextNode(
        "This is text with an image ![alt text](https://example.com/image.png) and another ![another image](https://example.com/another_image.png)",
        TextType.TEXT,
        )
        node2 = TextNode(
        "This is 2nd text with an image ![alt2 text2](https://ex2.com/image.png) and another ![another2 image2](https://ex3.com/ex3.png) END",
        TextType.TEXT,
        )
        self.assertEqual(split_nodes_image([node, node2]), [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("another image", TextType.IMAGE, "https://example.com/another_image.png"),
            TextNode("This is 2nd text with an image ", TextType.TEXT),
            TextNode("alt2 text2", TextType.IMAGE, "https://ex2.com/image.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("another2 image2", TextType.IMAGE, "https://ex3.com/ex3.png"),
            TextNode(" END", TextType.TEXT)
        ])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )        

    def test_text_to_textnodes(self):
        text = "This is **bold** text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(text_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ])
        text2 = "this is _italic_ and `code block` and **bold** and [link](https://example.com) or what ![image](https://example.com/image.png)"
        text_nodes2 = text_to_textnodes(text2)
        self.assertEqual(text_nodes2, [
            TextNode("this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" or what ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png")])

if __name__ == "__main__":
    unittest.main()
