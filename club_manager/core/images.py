# -*- coding: utf-8 -*-
"""
Module métier pour la gestion des images (logos, photos) dans Club Manager.
Permet de stocker, charger, supprimer et référencer les images utilisées dans l'application.
"""

import os
import shutil

IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "..", "resources", "images")

def save_image(src_path, dest_name):
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    dest_path = os.path.join(IMAGE_FOLDER, dest_name)
    shutil.copy(src_path, dest_path)
    return dest_path

def delete_image(image_name):
    path = os.path.join(IMAGE_FOLDER, image_name)
    if os.path.exists(path):
        os.remove(path)

def list_images():
    if not os.path.exists(IMAGE_FOLDER):
        return []
    return [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]