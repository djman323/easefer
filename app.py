import streamlit as st
import os
import time
from pathlib import Path
import streamlit.components.v1 as components
import base64

# Page config (MUST BE THE FIRST STREAMLIT COMMAND)
st.set_page_config(page_title="Easefer", page_icon="📁", layout="centered")

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

# File that tracks files to delete
DELETE_MARKER_FILE = ".delete_queue.txt"

# Helper functions
def mark_for_deletion(file_name):
    with open(DELETE_MARKER_FILE, "a") as f:
        f.write(file_name + "\n")

def get_files_marked_for_deletion():
    if not os.path.exists(DELETE_MARKER_FILE):
        return []
    with open(DELETE_MARKER_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def clear_deletion_list():
    if os.path.exists(DELETE_MARKER_FILE):
        os.remove(DELETE_MARKER_FILE)

# Custom CSS for Dark Theme
st.markdown("""
    <style>
    /* General Styling */
    body {
        font-family: 'Poppins', sans-serif;
        color: #e0e7ff;
    }

    .stApp {
        background: transparent;
        backdrop-filter: blur(10px);
    }

    /* Centered Header */
    h1 {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        color: #e0e7ff;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.4);
        margin-bottom: 0.5rem;
    }

    h3 {
        font-size: 1.8rem;
        font-weight: 600;
        color: #c7d2fe;
        margin-bottom: 1rem;
    }

    p {
        font-size: 1.1rem;
        color: #a5b4fc;
    }

    /* Glassmorphism Card Effect */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        border: 2px solid #ffffff; /* Solid white border as requested */
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 20px 0;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 1.2rem;
        font-weight: 500;
        color: #64748b;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"].stTabsActive {
        color: #e0e7ff;
        background: rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: #ffffff;
        font-weight: 600;
        border-radius: 10px;
        padding: 12px 24px;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #4338ca 0%, #6d28d9 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }

    .stDownloadButton button {
        background: linear-gradient(90deg, #059669 0%, #10b981 100%);
        color: #ffffff;
        font-weight: 600;
        border-radius: 10px;
        padding: 12px 24px;
        border: none;
        transition: all 0.3s ease;
    }

    .stDownloadButton button:hover {
        background: linear-gradient(90deg, #047857 0%, #059669 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }

    /* File Uploader */
    .stFileUploader {
        background: rgba(30, 41, 59, 0.7);
        border: 2px dashed rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: border 0.3s ease;
    }

    .stFileUploader:hover {
        border: 2px dashed #4f46e5;
    }

    /* Toggle Switch */
    .stToggle label {
        color: #a5b4fc;
        font-weight: 500;
    }

    /* Links */
    a {
        color: #818cf8;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }

    a:hover {
        color: #4f46e5;
    }

    /* Divider */
    .stMarkdown hr {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 2rem 0;
    }

    /* Streamlit Info/Warning Messages */
    .stAlert {
        background: rgba(255, 255, 255, 0.1);
        color: #e0e7ff;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Author
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file {image_path} not found. Please ensure the file exists in the same directory as this script.")
        return ""

img_base64 = get_base64_image("logo.png")

# Logo + title together
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
    <img src="data:image/png;base64,{img_base64}" width="75" style="border-radius: 20px;" />
    <h1 style="margin: 0;">Easefer</h1>
</div>
""", unsafe_allow_html=True)

st.markdown('<p style="text-align:center;">Transfer files between mobile and laptop with ease.</p>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;">Made with ❤️ by <a href="https://github.com/djman323" target="_blank">Devansh</a></div>', unsafe_allow_html=True)
st.markdown("---")

# State to track the last file check time
if "last_file_check" not in st.session_state:
    st.session_state.last_file_check = time.time()
if "last_files" not in st.session_state:
    st.session_state.last_files = set(os.listdir(UPLOAD_DIR))

# Polling mechanism to check for file changes every 5 seconds
def check_for_file_changes():
    current_time = time.time()
    if current_time - st.session_state.last_file_check >= 5:  # Check every 5 seconds
        current_files = set(os.listdir(UPLOAD_DIR))
        if current_files != st.session_state.last_files:
            st.session_state.last_files = current_files
            st.experimental_rerun()
        st.session_state.last_file_check = current_time

# Tabs
tabs = st.tabs(["🏠 Home", "📤 Upload", "📥 Files", "ℹ️ About"])

# --- Home Tab ---
with tabs[0]:
    st.markdown("""
    <div class="glass-card">
        <h3>🏠 Welcome</h3>
        <ul style="list-style-type: none; padding: 0;">
            <li>🔒 <strong>No login</strong> or account needed</li>
            <li>📂 <strong>Drag & drop</strong> or multi-select files</li>
            <li>🗑️ <strong>Auto-delete</strong> after download (optional)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- Upload Tab ---
with tabs[1]:
    st.markdown("""
    <div class="glass-card">
        <h3>📤 Upload Files</h3>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("Select one or more files to upload", accept_multiple_files=True)

    if st.button("📤 Upload"):
        if uploaded_files:
            for file in uploaded_files:
                file_path = os.path.join(UPLOAD_DIR, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
            st.success(f"✅ Uploaded {len(uploaded_files)} file(s) successfully.")
        else:
            st.warning("⚠️ Please select at least one file.")

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

# --- Files Tab ---
with tabs[2]:
    # Check for file changes to trigger auto-refresh
    check_for_file_changes()

    st.markdown("""
    <div class="glass-card">
        <h3>📥 Available Files</h3>
    """, unsafe_allow_html=True)
    
    delete_after = st.toggle("🗑️ Delete after download", value=True)

    # Clean up files marked from last run
    for file in get_files_marked_for_deletion():
        try:
            os.remove(os.path.join(UPLOAD_DIR, file))
        except FileNotFoundError:
            pass
    clear_deletion_list()

    files = os.listdir(UPLOAD_DIR)
    if not files:
        st.info("📭 No files available for download.")
    else:
        for file in files:
            with open(os.path.join(UPLOAD_DIR, file), "rb") as f:
                btn = st.download_button(
                    label=f"⬇️ Download {file}",
                    data=f,
                    file_name=file,
                    mime="application/octet-stream",
                    key=file
                )
            if btn and delete_after:
                mark_for_deletion(file)

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

# --- About Tab ---
with tabs[3]:
    st.markdown("""
    <div class="glass-card">
        <h3>ℹ️ About Easefer</h3>
        <p><strong>Easefer</strong> is a private, local file-sharing tool built with Python and Streamlit.</p>
        <p><strong>Key Features:</strong></p>
        <ul style="list-style-type: none; padding: 0;">
            <li>🎨 Clean and simple UI</li>
            <li>🏠 Runs locally on your network</li>
            <li>🔒 Fast and secure (your files stay on your machine)</li>
        </ul>
        <p>Want to contribute or raise an issue? Visit the <a href="https://github.com/djman323" target="_blank">GitHub repo</a>.</p>
    </div>
    """, unsafe_allow_html=True)