# -*- coding: utf-8 -*-
import os
import tempfile
from club_manager.core.images import save_image, delete_image, list_images, IMAGE_FOLDER

def test_save_delete_list_image(tmp_path, monkeypatch):
    # Crée une image temporaire
    img = tmp_path / "testimg.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")
    # Redirige IMAGE_FOLDER vers un dossier temporaire
    monkeypatch.setattr("club_manager.core.images.IMAGE_FOLDER", str(tmp_path))
    dest = save_image(str(img), "logo_test.png")
    assert os.path.exists(dest)
    assert "logo_test.png" in list_images()
    delete_image("logo_test.png")
    assert "logo_test.png" not in list_images()