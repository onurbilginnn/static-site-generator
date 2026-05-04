from re import findall

from textnode.textnode import TextType, TextNode
from htmlnode.htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {
            "href": f"{text_node.url}"
        })
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "",{
            "src": f"{text_node.url}",
            "alt": f"{text_node.text}"
        })
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        splitted_node_list = node.text.split(delimiter)
        if len(splitted_node_list) % 2 == 0:
            raise ValueError("Invalid markdown syntax!")
        for i, text in enumerate(splitted_node_list):
            if i % 2 == 0:
                new_nodes.append(TextNode(text, node.text_type))
            else:
                new_nodes.append(TextNode(text, text_type))
    return new_nodes

def extract_markdown_images(text):
    image_tuples = findall(r"!\[([^\]]*)\]\(([^)]+)\)", text)
    return image_tuples

def extract_markdown_links(text):
    link_tuples = findall(r"\[([^\]]*)\]\(([^)]+)\)", text)
    return link_tuples

def split_nodes_link(old_nodes):
    return create_split_nodes(old_nodes, extract_markdown_links, TextType.LINK)

def split_nodes_image(old_nodes):
    return create_split_nodes(old_nodes, extract_markdown_images, TextType.IMAGE)

def create_split_nodes(old_nodes, extract_markdown_items, type = TextType.LINK):
    result_nodes = []
    end_marker = -1 if type == TextType.LINK else -2
    for node in old_nodes:
        items = extract_markdown_items(node.text)
        if len(items) == 0:
            result_nodes.append(node)
            continue
        if len(items) > 0 and node.text_type != type:
            index = 0
            for link in items:
                split_text = node.text[index:].split(link[0], 1)
                index = node.text.find(link[1]) + len(link[1]) + 1
                result_nodes.append(TextNode(split_text[0][:end_marker], TextType.TEXT))
                result_nodes.append(TextNode(link[0], type, link[1]))
            last_text = node.text[index:]
            if last_text != "":
                result_nodes.append(TextNode(last_text, TextType.TEXT))
    return result_nodes

def text_to_textnodes(text):
    bold_split = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    image_split = split_nodes_image(code_split)
    return split_nodes_link(image_split)
    