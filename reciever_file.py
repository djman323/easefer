import streamlit as st
import threading
import socket
import os
import zipfile
from datetime import datetime

RECEIVED_DIR = "received_files"
LOG_FILE = "receiver_log.txt"
PORT = 9999

os.makedirs(RECEIVED_DIR, exist_ok=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")

def handle_client(client, addr):
    try:
        filename = client.recv(1024).decode()
        client.send(b'1')
        filesize = int(client.recv(1024).decode())
        client.send(b'1')

        filepath = os.path.join(RECEIVED_DIR, filename)
        with open(filepath, "wb") as f:
            received = 0
            while received < filesize:
                data = client.recv(1024 * 1024)
                if not data:
                    break
                f.write(data)
                received += len(data)

        if filename.endswith(".zip"):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                extract_dir = os.path.join(RECEIVED_DIR, filename.replace('.zip', ''))
                zip_ref.extractall(extract_dir)
            os.remove(filepath)
            log(f"Received and extracted: {filename}")
        else:
            log(f"Received file: {filename}")
    except Exception as e:
        log(f"Error from {addr}: {str(e)}")
    finally:
        client.close()

def start_server():
    s = socket.socket()
    s.bind(('0.0.0.0', PORT))
    s.listen(5)
    log("Server started on port 9999.")
    while True:
        client, addr = s.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()

# Streamlit UI
st.title("📥 Streamlit File Receiver")
st.info(f"🖥️ Your IP Address (share with sender): **{get_local_ip()}**")

if st.button("🚀 Start Receiver Server"):
    threading.Thread(target=start_server, daemon=True).start()
    st.success("Receiver server started and listening on port 9999.")

st.subheader("📄 Transfer Logs")
if os.path.exists(LOG_FILE):
    with open(LOG_FILE) as f:
        st.text(f.read())
else:
    st.info("No logs yet.")

st.subheader("📁 Received Files")
for root, dirs, files in os.walk(RECEIVED_DIR):
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, RECEIVED_DIR)
        with open(full_path, "rb") as f:
            st.download_button(f"⬇️ Download {rel_path}", f, file_name=rel_path)
