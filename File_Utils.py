import os
import hashlib

def calculate_file_hash(file_path):
    """Return SHA256 hash of a file"""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()


def get_all_files(folder):
    """Return dictionary of file -> hash"""
    files = {}
    for root, _, filenames in os.walk(folder):
        for file in filenames:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, folder)
            files[rel_path] = calculate_file_hash(path)
    return files


def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def write_file(base_folder, relative_path, data):
    full_path = os.path.join(base_folder, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "wb") as f:
        f.write(data)
