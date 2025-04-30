import streamlit as st
import os
from PIL import Image
from utils.face_utils import save_image, get_all_images, find_matching_images

# Set up folder
IMAGE_STORE = "image_store"
os.makedirs(IMAGE_STORE, exist_ok=True)

st.set_page_config(page_title="Photo Search App", layout="wide")
st.title("📷 Photo Search & Upload App")

tabs = st.tabs(["📤 Upload Image", "🖼️ View All Images", "🔍 Search by Face"])

# --- Upload Tab ---
with tabs[0]:
    st.header("Upload Images")
    username = st.text_input("Enter your name or username", max_chars=30)

    uploaded_files = st.file_uploader("Upload one or more images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if username and uploaded_files:
        for uploaded_file in uploaded_files:
            save_image(uploaded_file, username)
        st.success(f"{len(uploaded_files)} image(s) uploaded for {username}")

# --- View Tab ---
with tabs[1]:
    st.header("All Uploaded Images")
    all_images = get_all_images(IMAGE_STORE)
    if all_images:
        for user, imgs in all_images.items():
            st.subheader(f"👤 {user}")
            cols = st.columns(4)
            for idx, img_path in enumerate(imgs):
                with cols[idx % 4]:
                    st.image(img_path, use_column_width=True)
    else:
        st.info("No images uploaded yet.")

# --- Search Tab ---
with tabs[2]:
    st.header("Search Images by Face")
    search_img = st.file_uploader("Upload an image with your face", type=["jpg", "jpeg", "png"])

    if search_img:
        with st.spinner("Searching for matches..."):
            matches = find_matching_images(search_img, IMAGE_STORE)
        if matches:
            st.success(f"Found {len(matches)} matching image(s)")
            cols = st.columns(4)
            for idx, match_path in enumerate(matches):
                with cols[idx % 4]:
                    st.image(match_path, use_column_width=True)
        else:
            st.warning("No matches found.")
