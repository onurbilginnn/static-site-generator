import sys

from utils import delete_all_files_in_directory, copy_all_files_in_directory, generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    delete_all_files_in_directory("./docs")
    copy_all_files_in_directory("./static", "./docs")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


if __name__ == "__main__":
    main()

