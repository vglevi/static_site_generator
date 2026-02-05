import os
import shutil
from page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def copy_contents(src, dst):
    if not os.path.exists(src):
        raise Exception("The source doesn't exist")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for path in os.listdir(src):
        src_path = os.path.join(src, path)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst)
        else:
            copy_contents(src_path, os.path.join(dst, path))


def main():
    copy_contents(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()
