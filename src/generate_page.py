import re
import os
from pathlib import Path
from markdown_to_blocks import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """Extracts the first level-1 heading (#) as the title."""
    title_match = re.search(r'^#\s+(.+)', markdown, re.MULTILINE)
    if not title_match:
        raise ValueError("Title not found in markdown. Make sure there's a '# Title' at the top.")
    return title_match.group(1).strip()


def generate_page(from_path: Path, template_path: Path, dest_path: Path, basepath: str = "/") -> None:
    """Generates an HTML page from a markdown file using a template."""
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    markdown_content = from_path.read_text(encoding='utf-8')
    template_content = template_path.read_text(encoding='utf-8')

    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)

    if "{{Title}}" not in template_content or "{{Content}}" not in template_content:
        raise ValueError("Template missing {{Title}} or {{Content}} placeholder")

    final_html = (
        template_content
        .replace("{{Title}}", title)
        .replace("{{Content}}", html_string)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(final_html, encoding='utf-8')



def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path, basepath: str = "/"):
    template_content = template_path.read_text(encoding='utf-8')

    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                md_path = Path(root) / file
                relative_path = md_path.relative_to(dir_path_content)
                dest_path = dest_dir_path / relative_path.with_suffix('.html')

                md_content = md_path.read_text(encoding='utf-8')
                html_node = markdown_to_html_node(md_content)
                html_string = html_node.to_html()
                title = extract_title(md_content)

                if "{{Title}}" not in template_content or "{{Content}}" not in template_content:
                    raise ValueError("Template missing {{Title}} or {{Content}} placeholder")

                final_html = (
                    template_content
                    .replace("{{Title}}", title)
                    .replace("{{Content}}", html_string)
                    .replace('href="/', f'href="{basepath}')
                    .replace('src="/', f'src="{basepath}')
                )

                dest_path.parent.mkdir(parents=True, exist_ok=True)
                dest_path.write_text(final_html, encoding='utf-8')
