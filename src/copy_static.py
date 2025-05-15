import os

def clear_directory(directory: str):
    """Deletes all contents of the specified directory."""
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)
            print(f"Deleted {file_path}")
        for name in dirs:
            dir_path = os.path.join(root, name)
            os.rmdir(dir_path)
            print(f"Deleted directory {dir_path}")

def copy_directory_contents(source_dir: str, dest_dir: str):
    """Recursively copies all files and subdirectories from source to destination."""
    # Clear the destination directory before copying
    if os.path.exists(dest_dir):
        clear_directory(dest_dir)
    else:
        os.makedirs(dest_dir)  # If the destination directory does not exist, create it

    # Iterate over the items in the source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(source_path):
            # If it's a directory, create the corresponding directory in the destination
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            # Recursively copy the subdirectory contents
            copy_directory_contents(source_path, dest_path)
        else:
            # If it's a file, copy it to the destination
            with open(source_path, 'rb') as fsrc:
                with open(dest_path, 'wb') as fdst:
                    # Read the source file and write to the destination
                    while True:
                        buf = fsrc.read(1024*1024)  # Read in chunks
                        if not buf:
                            break
                        fdst.write(buf)


