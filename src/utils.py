import os

from htmlnode.htmlnode import LeafNode, ParentNode
from textnode.utils import text_to_textnodes, text_node_to_html_node
from markdown.utils import is_block_heading
from markdown.markdown import BlockType, markdown_to_blocks, \
    block_to_block_type

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    parent_div = ParentNode("div", [])
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            header_number = is_block_heading(block)
            parent_div.children.append(LeafNode(f"h{header_number}", block[header_number + 1:]))
        elif block_type == BlockType.CODE:
            code_parent = ParentNode("pre", [])
            code_parent.children.append(LeafNode("code", block[4:-3]))
            parent_div.children.append(code_parent)
        elif block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
            list_tag = "ul" if block_type == BlockType.UNORDERED_LIST else "ol"
            list_parent = ParentNode(list_tag, [])
            list_items = block.split("\n")
            for item in list_items:
                start_index = 2 if block_type == BlockType.UNORDERED_LIST else 3
                text_nodes = text_to_textnodes(item[start_index:])
                item_parent = ParentNode("li", [])
                for node in text_nodes:
                    item_parent.children.append(text_node_to_html_node(node))
                list_parent.children.append(item_parent)
            parent_div.children.append(list_parent)
        elif block_type == BlockType.QUOTE:
            raw_text = block.replace("\n", " ")
            text_nodes = text_to_textnodes(raw_text)
            quote_parent = ParentNode("blockquote", [])
            for node in text_nodes:
                modified_node_text = node.text.replace("> ", "")
                node.text = modified_node_text.replace(">", "")
                quote_parent.children.append(text_node_to_html_node(node))
            parent_div.children.append(quote_parent)
        else:
            raw_text = block.replace("\n", " ")
            text_nodes = text_to_textnodes(raw_text)
            paragraph_parent = ParentNode("p", [])
            for node in text_nodes:
                paragraph_parent.children.append(text_node_to_html_node(node))
            parent_div.children.append(paragraph_parent)
    return parent_div


def delete_all_files_in_directory(dir_path):
    if os.path.exists(dir_path) is False:
        raise FileExistsError("Directory not exists")
    if os.path.isfile(dir_path):
        print(f"Deleting file {dir_path}")
        os.remove(dir_path)
    else:
        items_in_dir = os.listdir(dir_path)
        for item in items_in_dir:
            item_path = os.path.join(dir_path, item)
            delete_all_files_in_directory(item_path)
        if os.path.isfile(dir_path) is False:
            os.rmdir(dir_path)

def copy_all_files_in_directory(src_dir, dest_dir):
    if os.path.exists(dest_dir) is False:
        os.mkdir(dest_dir)
    items_in_src_dir = os.listdir(src_dir)
    for item in items_in_src_dir:
        src_item_path = os.path.join(src_dir, item)
        dest_item_path = os.path.join(dest_dir, item)
        if os.path.isfile(src_item_path):
            print(f"Copying file from {src_item_path} to {dest_item_path}")
            with open(src_item_path, "rb") as src_file:
                with open(dest_item_path, "wb") as dest_file:
                    dest_file.write(src_file.read())
        else:
            copy_all_files_in_directory(src_item_path, dest_item_path)

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        if block[:2] == "# ":
            return block[2:].strip()
    raise Exception("There is no header present!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_text = ""
    template_text = ""
    with open(from_path, "r") as markdown_file:
        markdown_text = markdown_file.read()
    with open(template_path, "r") as template_file:
        template_text = template_file.read()
    html_node = markdown_to_html_node(markdown_text)
    html = html_node.to_html()
    title = extract_title(markdown_text)
    modified_template = template_text.replace("{{ Title }}", title).replace("{{ Content }}", html)
    with open(dest_path, "w") as dest_file:
        dest_file.write(modified_template)

def generate_pages_recursive(dir_path, template_path, dest_dir):
    if os.path.isfile(dir_path):
        if dir_path.endswith(".md"):
            file_name = os.path.basename(dir_path)
            parent_path = os.path.split(dir_path)[0].replace("./content", dest_dir)
            if os.path.exists(parent_path) is False:
                os.makedirs(parent_path)
            dest_path = os.path.join(parent_path, file_name[:-3] + ".html")
            generate_page(dir_path, template_path, dest_path)
    else:
        items_in_dir = os.listdir(dir_path)
        for item in items_in_dir:
            item_path = os.path.join(dir_path, item)
            generate_pages_recursive(item_path, template_path, dest_dir)