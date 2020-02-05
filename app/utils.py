import os
import secrets
from flask import current_app
from PIL import Image


def save_picture(pic, pic_type):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(pic.filename)
    picture_fname = random_hex + f_ext
    if pic_type == "profile":
        picture_path = os.path.join(current_app.root_path, 'static/profile_pic', picture_fname)
        output_size = (250, 250)
    elif pic_type == "event":
        picture_path = os.path.join(current_app.root_path, 'static/event_thumbnail', picture_fname)
        output_size = (1920, 1080)
    else:
        return

    image = Image.open(pic)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fname
