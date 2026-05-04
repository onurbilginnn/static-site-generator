from enum import Enum

from markdown.utils import is_block_code, \
      is_block_heading, \
      is_block_unorderedlist, \
      is_block_orderedlist, \
      is_block_quote

class BlockType(Enum):
    PARAGRAPH = ""
    HEADING = "######"
    CODE = "```"
    QUOTE = ">"
    UNORDERED_LIST = "-"
    ORDERED_LIST = "."



def markdown_to_blocks(markdown):
    markdown_texts = markdown.split("\n\n")
    result_texts = []
    for text in markdown_texts:
        if text == "":
            continue
        if text[0] == "\n":
            text = text[1:]
        if text[-1] == "\n":
            text = text[:-1]
        result_texts.append(text.strip(" "))
    return result_texts


def block_to_block_type(block):
    if is_block_heading(block) > 0:
        return BlockType.HEADING
    if is_block_code(block):
        return BlockType.CODE
    if is_block_quote(block):
        return BlockType.QUOTE
    if is_block_unorderedlist(block):
        return BlockType.UNORDERED_LIST
    if is_block_orderedlist(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


