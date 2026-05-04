import unittest

from utils import markdown_to_html_node, extract_title


class TestTextNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        md = """
tag here

# Header1

This is another paragraph with _italic_ text and `code` here

"""
        header = extract_title(md)
        self.assertEqual(
            header, "Header1")
        
        md2 = """
# Header2

tag here

This is another paragraph with _italic_ text and `code` here

"""
        header2 = extract_title(md2)
        self.assertEqual(
            header2, "Header2")

        md3 = """
## Header3

tag here

This is another paragraph with _italic_ text and `code` here

"""
        with self.assertRaises(Exception) as context:
            extract_title(md3)
        self.assertEqual(context.exception.args[0],
                         "There is no header present!")

        md4 = """
tag here

This is another paragraph with _italic_ text and `code` here

# Header4

"""
        header4 = extract_title(md4)
        self.assertEqual(
            header4, "Header4")
        
if __name__ == "__main__":
    unittest.main()
