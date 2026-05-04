from textnode.textnode import TextNode, TextType
from utils import delete_all_files_in_directory, copy_all_files_in_directory, generate_pages_recursive

def main():
    # delete_all_files_in_directory("./public")
    # copy_all_files_in_directory("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()

