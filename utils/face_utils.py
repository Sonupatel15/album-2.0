import os
import face_recognition
import numpy as np
from PIL import Image
import shutil
import uuid

def save_image(uploaded_file, username):
    user_folder = os.path.join("image_store", username)
    os.makedirs(user_folder, exist_ok=True)

    file_ext = uploaded_file.name.split(".")[-1]
    unique_name = f"{uuid.uuid4().hex}.{file_ext}"
    filepath = os.path.join(user_folder, unique_name)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)

def get_all_images(base_folder):
    all_data = {}
    for user in os.listdir(base_folder):
        user_folder = os.path.join(base_folder, user)
        if os.path.isdir(user_folder):
            image_paths = [
                os.path.join(user_folder, fname)
                for fname in os.listdir(user_folder)
                if fname.lower().endswith(("jpg", "jpeg", "png"))
            ]
            if image_paths:
                all_data[user] = image_paths
    return all_data

def get_face_encodings(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        return encodings
    except Exception:
        return []

def find_matching_images(search_image_file, base_folder, tolerance=0.6):
    try:
        search_img = face_recognition.load_image_file(search_image_file)
        search_encodings = face_recognition.face_encodings(search_img)
        if not search_encodings:
            return []
        search_encoding = search_encodings[0]
    except Exception:
        return []

    matching_images = []
    for user in os.listdir(base_folder):
        user_folder = os.path.join(base_folder, user)
        if os.path.isdir(user_folder):
            for fname in os.listdir(user_folder):
                if fname.lower().endswith(("jpg", "jpeg", "png")):
                    img_path = os.path.join(user_folder, fname)
                    encodings = get_face_encodings(img_path)
                    for face_encoding in encodings:
                        match = face_recognition.compare_faces([search_encoding], face_encoding, tolerance=tolerance)
                        if match[0]:
                            matching_images.append(img_path)
                            break
    return matching_images
