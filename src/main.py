from copy_static import copy_directory_contents
from generate_page import generate_pages_recursive
from pathlib import Path


def main():
    source_directory = Path('static')
    destination_directory = Path('public')

    print("Copying static assets...")
    copy_directory_contents(source_directory, destination_directory)
    print("Static assets copied.")

    dir_path_content = Path("content")
    template_path = Path("template.html")
    dest_dir_path = Path("public")
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)


if __name__ == "__main__":
    main()
