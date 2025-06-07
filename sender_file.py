import streamlit as st
import socket
import os

# Helper to get local IP
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

def send_single_file(file, ip):
    filename = file.name
    filesize = len(file.getbuffer())

    s = socket.socket()
    s.connect((ip, 9999))

    s.send(filename.encode())
    s.recv(1)
    s.send(str(filesize).encode())
    s.recv(1)

    bytes_sent = 0
    chunk_size = 1024 * 1024
    progress_bar = st.progress(0)

    file.seek(0)
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        s.sendall(chunk)
        bytes_sent += len(chunk)
        percent = int(bytes_sent / filesize * 100)
        progress_bar.progress(min(percent, 100))

    s.close()

# Streamlit UI
st.title("📤 Streamlit File Sender")
st.info(f"🔌 Your IP Address: **{get_local_ip()}** (Share this with the receiver)")

receiver_ip = st.text_input("Enter Receiver's IP", "127.0.0.1")
uploaded_files = st.file_uploader("Choose files to send", accept_multiple_files=True)

if st.button("Send Files"):
    if not uploaded_files:
        st.warning("No files selected.")
    else:
        with st.spinner("Sending files..."):
            for file in uploaded_files:
                file.seek(0)
                send_single_file(file, receiver_ip)
            st.success("✅ All files sent successfully!")

        st.subheader("📄 Transfer Logs")
        if os.path.exists("sender_log.txt"):
            with open("sender_log.txt") as f:
                st.text(f.read())
        else:
            st.info("No logs yet.")