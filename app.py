import streamlit as st
import os
from pathlib import Path

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

# Page config and title
st.set_page_config(page_title="Easefer | File Transfer", layout="centered")#page_icon="📤"
st.title(" Easefer - Upload & Share Files")
st.caption("Easily transfer files between mobile and laptop over the web.")

# Upload section
st.header(" Upload Files")
uploaded_files = st.file_uploader("Select files", accept_multiple_files=True)

if st.button("Upload"):
    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_DIR, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f" {len(uploaded_files)} file(s) uploaded successfully.")
    else:
        st.warning("Please select file(s) first.")

# List files available for download
st.header(" Available Files to Download In your Network")

files = os.listdir(UPLOAD_DIR)
if not files:
    st.info("No files uploaded yet.")
else:
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file)
        with open(file_path, "rb") as f:
            st.download_button(
                label=f"⬇️ {file}",
                data=f,
                file_name=file,
                mime="application/octet-stream"
            )
