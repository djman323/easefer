import streamlit as st
import os
import time
from pathlib import Path
import streamlit.components.v1 as components
import base64
import zipfile
from io import BytesIO
import hashlib

# Page config (MUST BE THE FIRST STREAMLIT COMMAND)
st.set_page_config(page_title="Easefer", page_icon="📁", layout="centered")

# Base directory to store uploaded files
BASE_UPLOAD_DIR = "uploaded_files"

# Generate a unique device code
def generate_device_code():
    session_id = st.session_state.get("session_id", str(id(st.session_state)))
    timestamp = str(time.time())
    hash_input = (session_id + timestamp).encode("utf-8")
    device_code = hashlib.md5(hash_input).hexdigest()[:8]
    return device_code

# Initialize device code in session state
if "device_code" not in st.session_state:
    st.session_state.device_code = generate_device_code()

DEVICE_CODE = st.session_state.device_code
UPLOAD_DIR = os.path.join(BASE_UPLOAD_DIR, DEVICE_CODE)
Path(UPLOAD_DIR).mkdir(exist_ok=True)

# Function to create a ZIP file of all files in a directory
def create_zip_of_files(directory):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                zip_file.write(file_path, file)
    buffer.seek(0)
    return buffer

# Function to generate file preview
def get_file_preview(file_path):
    if not os.path.exists(file_path):
        return None
    
    file_name = os.path.basename(file_path)
    try:
        file_size = os.path.getsize(file_path) / 1024
    except FileNotFoundError:
        return None
    
    extension = file_name.split(".")[-1].lower() if "." in file_name else ""

    if extension in ["png", "jpg", "jpeg"]:
        try:
            with open(file_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            return f'<img src="data:image/{extension};base64,{img_data}" width="100" style="border-radius: 5px; object-fit: cover;" />'
        except FileNotFoundError:
            return None
    
    elif extension in ["txt", "md"]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(100)
                if len(content) == 100:
                    content += "..."
                return f'<p style="font-size: 0.9rem; color: #a5b4fc;">{content}</p>'
        except (FileNotFoundError, Exception):
            return f'<p style="font-size: 0.9rem; color: #a5b4fc;">(Unable to read text)</p>'
    
    else:
        return f'<p style="font-size: 0.9rem; color: #a5b4fc;">Size: {file_size:.2f} KB</p>'

# Custom CSS for Dark Theme
st.markdown("""
    <style>
    body {
        font-family: 'Poppins', sans-serif;
        color: #e0e7ff;
    }
    .stApp {
        background: transparent;
        backdrop-filter: blur(10px);
    }
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
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        border: 2px solid #ffffff;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 20px 0;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
    }
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
    .stToggle label {
        color: #a5b4fc;
        font-weight: 500;
    }
    a {
        color: #818cf8;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    a:hover {
        color: #4f46e5;
    }
    .stMarkdown hr {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 2rem 0;
    }
    .stAlert {
        background: rgba(255, 255, 255, 0.1);
        color: #e0e7ff;
        border-radius: 10px;
    }
    .file-preview-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    .file-preview-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .file-preview-card:hover {
        transform: scale(1.05);
    }
    .file-preview-card img {
        max-width: 100%;
        height: 100px;
        object-fit: cover;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .file-preview-card p {
        margin: 5px 0;
        font-size: 0.9rem;
        color: #a5b4fc;
    }
    .device-code {
        font-size: 1rem;
        font-weight: 500;
        color: #a5b4fc;
        text-align: center;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Title, Author, and Device Code
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file {image_path} not found. Please ensure the file exists in the same directory as this script.")
        return ""

img_base64 = get_base64_image("logo.png")

st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
    <img src="data:image/png;base64,{img_base64}" width="75" style="border-radius: 20px;" />
    <h1 style="margin: 0;">Easefer</h1>
</div>
<div class="device-code">Your Device Code: <strong>{DEVICE_CODE}</strong></div>
""", unsafe_allow_html=True)

st.markdown('<p style="text-align:center;">Transfer files between mobile and laptop with ease.</p>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;">Made with ❤️ by <a href="https://github.com/djman323" target="_blank">Devansh</a></div>', unsafe_allow_html=True)
st.markdown("---")

# State to track the last file check times for Files tab
if "last_file_check_own" not in st.session_state:
    st.session_state.last_file_check_own = time.time()
if "last_files_own" not in st.session_state:
    st.session_state.last_files_own = set()

# Polling mechanism to check for file changes every 5 seconds (for Files tab only)
def check_for_file_changes(directory, last_check_key, last_files_key):
    try:
        current_files = set([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    except FileNotFoundError:
        st.session_state[last_files_key] = set()
        return False
    
    current_time = time.time()
    if current_time - st.session_state[last_check_key] >= 5:
        if current_files != st.session_state[last_files_key]:
            st.session_state[last_files_key] = current_files
            st.session_state[last_check_key] = current_time
            return True
        st.session_state[last_check_key] = current_time
    return False

# Tabs
tabs = st.tabs(["🏠 Home", "📤 Upload", "📥 Files", "🔄 Share", "ℹ️ About"])

# --- Home Tab ---
with tabs[0]:
    st.markdown("""
    <div class="glass-card">
        <h3>🏠 Welcome</h3>
        <ul style="list-style-type: none; padding: 0;">
            <li>🔒 <strong>No login</strong> or account needed</li>
            <li>📂 <strong>Drag & drop</strong> or multi-select files</li>
            <li>🗑️ <strong>Auto-delete</strong> after download (optional)</li>
            <li>🔄 Share files by exchanging device codes</li>
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
    delete_after_upload = st.toggle("🗑️ Delete after upload", value=False)

    if st.button("📤 Upload"):
        if uploaded_files:
            for file in uploaded_files:
                file_path = os.path.join(UPLOAD_DIR, file.name)
                try:
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                    if delete_after_upload:
                        try:
                            os.remove(file_path)
                        except FileNotFoundError:
                            pass
                except Exception as e:
                    st.error(f"Failed to upload {file.name}: {str(e)}")
            st.success(f"✅ Uploaded {len(uploaded_files)} file(s) successfully.")
            if delete_after_upload:
                st.rerun()
        else:
            st.warning("⚠️ Please select at least one file.")

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

# --- Files Tab ---
with tabs[2]:
    if check_for_file_changes(UPLOAD_DIR, "last_file_check_own", "last_files_own"):
        st.rerun()

    st.markdown("""
    <div class="glass-card">
        <h3>📥 Your Files</h3>
    """, unsafe_allow_html=True)
    
    delete_after_download = st.toggle("🗑️ Delete after download", value=True)

    files = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
    if not files:
        st.info("📭 No files available for download.")
    else:
        zip_buffer = create_zip_of_files(UPLOAD_DIR)
        btn = st.download_button(
            label="⬇️ Download All Files",
            data=zip_buffer,
            file_name="all_files.zip",
            mime="application/zip",
            key="download_all"
        )
        if btn:
            st.rerun()

        st.markdown('<div class="file-preview-grid">', unsafe_allow_html=True)
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file)
            if not os.path.exists(file_path):
                continue
            preview = get_file_preview(file_path)
            if preview is None:
                continue
            st.markdown(f"""
            <div class="file-preview-card">
                {preview}
                <p style="font-size: 0.9rem; color: #c7d2fe;">{file}</p>
            """, unsafe_allow_html=True)
            
            try:
                with open(file_path, "rb") as f:
                    btn = st.download_button(
                        label=f"⬇️ Download",
                        data=f,
                        file_name=file,
                        mime="application/octet-stream",
                        key=f"download_{file}"
                    )
                if btn:
                    st.rerun()
            except FileNotFoundError:
                continue
            
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

# --- Share Tab ---
with tabs[3]:
    st.markdown("""
    <div class="glass-card">
        <h3>🔄 Share Files</h3>
        <p>Enter another device's code to access their files.</p>
    """, unsafe_allow_html=True)

    # Initialize shared device code in session state if not present
    if "shared_device_code" not in st.session_state:
        st.session_state.shared_device_code = ""

    other_device_code = st.text_input("Enter Device Code", placeholder="e.g., a1b2c3d4", key="share_code_input", value=st.session_state.shared_device_code)

    # Update the shared device code in session state
    if other_device_code != st.session_state.shared_device_code:
        st.session_state.shared_device_code = other_device_code
        st.rerun()

    if other_device_code:
        other_device_dir = os.path.join(BASE_UPLOAD_DIR, other_device_code)
        if not os.path.exists(other_device_dir):
            st.error("Invalid device code or no files available.")
        else:
            other_files = [f for f in os.listdir(other_device_dir) if os.path.isfile(os.path.join(other_device_dir, f))]
            
            if not other_files:
                st.info("📭 No files available from this device.")
            else:
                zip_buffer = create_zip_of_files(other_device_dir)
                btn = st.download_button(
                    label=f"⬇️ Download All Files from {other_device_code}",
                    data=zip_buffer,
                    file_name=f"files_from_{other_device_code}.zip",
                    mime="application/zip",
                    key=f"download_all_shared_{other_device_code}"
                )
                if btn:
                    st.rerun()

                st.markdown('<div class="file-preview-grid">', unsafe_allow_html=True)
                for file in other_files:
                    file_path = os.path.join(other_device_dir, file)
                    if not os.path.exists(file_path):
                        continue
                    preview = get_file_preview(file_path)
                    if preview is None:
                        continue
                    st.markdown(f"""
                    <div class="file-preview-card">
                        {preview}
                        <p style="font-size: 0.9rem; color: #c7d2fe;">{file}</p>
                    """, unsafe_allow_html=True)
                    
                    try:
                        with open(file_path, "rb") as f:
                            btn = st.download_button(
                                label=f"⬇️ Download",
                                data=f,
                                file_name=file,
                                mime="application/octet-stream",
                                key=f"download_shared_{other_device_code}_{file}"
                            )
                        if btn:
                            st.rerun()
                    except FileNotFoundError:
                        continue
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

# --- About Tab ---
with tabs[4]:
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