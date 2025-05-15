from copy_static import copy_directory_contents
from generate_page import generate_pages_recursive
from pathlib import Path
import sys


def main():
    source_directory = Path('static')
    destination_directory = Path('docs')

    print("Copying static assets...")
    copy_directory_contents(source_directory, destination_directory)
    print("Static assets copied.")

    # Read basepath from command-line args, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Ensure basepath ends with a slash if it's not root
    if not basepath.endswith("/"):
        basepath += "/"

    dir_path_content = Path("content")
    template_path = Path("template.html")
    dest_dir_path = Path("docs")
    print (f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)
    print ("Pages generated")


if __name__ == "__main__":
    main()
