import os
import numpy as np
from PIL import Image
import shutil
import uuid
from deepface import DeepFace

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

def find_matching_images(search_image_file, base_folder, model_name="VGG-Face", threshold=0.6):
    matching_images = []

    # Save uploaded file temporarily
    temp_path = "temp_search.jpg"
    with open(temp_path, "wb") as f:
        f.write(search_image_file.read())

    for user in os.listdir(base_folder):
        user_folder = os.path.join(base_folder, user)
        if os.path.isdir(user_folder):
            for fname in os.listdir(user_folder):
                if fname.lower().endswith(("jpg", "jpeg", "png")):
                    img_path = os.path.join(user_folder, fname)
                    try:
                        result = DeepFace.verify(temp_path, img_path, model_name=model_name, enforce_detection=False)
                        if result["verified"] and result["distance"] <= threshold:
                            matching_images.append(img_path)
                    except Exception as e:
                        print(f"Error comparing {img_path}: {e}")
                        continue

    os.remove(temp_path)
    return matching_images
