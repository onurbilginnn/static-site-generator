def is_block_heading(block):
    for i in range(6):
        heading_block = "#" * (i + 1)
        if block[:i+2] == heading_block + " ":
            return i + 1
    return 0

def is_block_code(block):
    code_block = "```"
    if block[:4] == f"{code_block}\n" and \
        block[-4:] == f"\n{code_block}":
        return True
    return False

def is_block_quote(block):
    quote_block = ">"
    if block[:1] == quote_block:
        return True
    return False

def is_block_unorderedlist(block):
    list_block = "- "
    if block[:2] == list_block:
        return True
    return False

def is_block_orderedlist(block):
    list_block = ". "
    if block[0].isdigit() and block[1:3] == list_block:
        return True
    return False
