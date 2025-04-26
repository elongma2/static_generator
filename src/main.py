from textnode import TextNodeType,TextNode 
from htmlnode import LeafNode
import os 
import shutil
from helper_func import generate_page,generate_pages_recursive
import sys

def main (): 
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    # get path
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../static")
    dest_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../docs")

    # convert to abs
    src_path = os.path.abspath(src_path)
    dest_path = os.path.abspath(dest_path)

    # ✅ Ensure destination folder exists first
    os.makedirs(dest_path, exist_ok=True)

    # delete files
    delete_files(dest_path)

    # copy files
    copy_function(src_path, dest_path)

    # generate page
    from_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../content")
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../template.html")
    
    generate_pages_recursive(from_path, template_path, dest_path, base_path)

    print("Done")



def delete_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            print(f"Deleted: {file_path}")

    

def copy_function(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        if os.path.isdir(src_path):
            copy_function(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)
            print(f"Copied: {src_path} → {dest_path}")

if __name__ == "__main__":
    main()