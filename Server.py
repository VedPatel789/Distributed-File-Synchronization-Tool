import socket
import json
import os

from config import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, SYNC_FOLDER
from file_utils import get_all_files, ensure_folder, write_file

ensure_folder(SYNC_FOLDER)

def handle_client(conn):
    data = conn.recv(BUFFER_SIZE).decode()
    request = json.loads(data)

    client_files = request.get("files", {})

    server_files = get_all_files(SYNC_FOLDER)

    # Determine missing or outdated files
    to_send = []

    for file, c_hash in client_files.items():
        s_hash = server_files.get(file)
        if s_hash != c_hash:
            full_path = os.path.join(SYNC_FOLDER, file)
            if os.path.exists(full_path):
                with open(full_path, "rb") as f:
                    content = f.read()
                to_send.append((file, content))

    response = json.dumps({
        "files": [(f, c.decode("latin1")) for f, c in to_send]
    })

    conn.send(response.encode())
    conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)

    print(f"[SERVER] Running on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[CONNECTED] {addr}")
        handle_client(conn)


if __name__ == "__main__":
    start_server()
