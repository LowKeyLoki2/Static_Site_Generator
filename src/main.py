from copy_static import copy_directory_contents
from generate_page import generate_page
from pathlib import Path


def main():
    source_directory = Path('static')
    destination_directory = Path('public')

    print("Copying static assets...")
    copy_directory_contents(source_directory, destination_directory)
    print("Static assets copied.")

    # Ensure the public directory exists
    destination_directory.mkdir(parents=True, exist_ok=True)

    # Define input/output paths
    content_file = Path('content/index.md')
    template_file = Path('template.html')
    output_file = destination_directory / 'index.html'

    print(f"Generating HTML page: {output_file}")
    generate_page(content_file, template_file, output_file)
    print("Page generation complete.")


if __name__ == "__main__":
    main()
