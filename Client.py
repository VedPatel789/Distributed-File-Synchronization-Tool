import socket
import json
import os

from config import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, SYNC_FOLDER
from file_utils import get_all_files, ensure_folder, write_file

ensure_folder(SYNC_FOLDER)

def sync_with_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    local_files = get_all_files(SYNC_FOLDER)

    request = json.dumps({"files": local_files})
    client.send(request.encode())

    response = client.recv(BUFFER_SIZE).decode()
    data = json.loads(response)

    updates = data.get("files", [])

    for filename, content in updates:
        write_file(SYNC_FOLDER, filename, content.encode("latin1"))
        print(f"[UPDATED] {filename}")

    client.close()


if __name__ == "__main__":
    sync_with_server()
