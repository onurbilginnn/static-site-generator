import unittest

from markdown.markdown import markdown_to_blocks, \
      block_to_block_type, \
        BlockType


class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        md2 = """"""
        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(
            blocks2,
            [],
        )
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("###### test"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("# test"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\n test\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\n test```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(">test"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> test"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("-test"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- test"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(". test"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(".test"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("test"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
