import os
from block_markdown import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()
    
    html = markdown_to_html_node(md).to_html() 
    title = extract_title(md)
    
    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("Content directory doesn't exist")
    for path in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, path)
        if os.path.isfile(from_path):
            if from_path[-3:] == ".md":
                html_path = os.path.join(dest_dir_path, path.replace(".md", ".html"))
                generate_page(from_path, template_path, html_path)
        else:
            to_path = os.path.join(dest_dir_path, path)
            generate_pages_recursive(from_path, template_path, to_path)
