# Distributed File Synchronization Tool

A simple Python-based distributed file synchronization system using TCP sockets and SHA256 hashing.

## Features

- Sync files between client and server
- Detects file changes using hashing
- Lightweight (no external libraries)
- Works on LAN / same network

---

## How It Works

1. Client scans local folder (`sync_folder`)
2. Sends file hashes to server
3. Server compares with its own folder
4. Server sends updated files back
5. Client updates missing/outdated files

---

## Run Server

```bash
python server.py
