import functools
import os
from functools import wraps
import datetime
from flask import redirect, session, url_for
from PIL import Image
from datetime import datetime
from datetime import date
import random
from captcha.image import ImageCaptcha
import base64
from extensions import db
from models.member import *
from models.blog import *


def resize_image(input_folder, size_f_t, output_folder):
    global new_height, output_filepath
    if input_folder[-1] != '/':
        input_folder = input_folder + '/'
    all_images = os.listdir(input_folder)
    if output_folder[-1] != '/':
        output_folder = output_folder + '/'

    for a in all_images:
        image_path = input_folder + a

        if a.endswith(".jpg") or a.endswith(".png"):

            fixed_full_height = 900
            fixed_thumbnail_height = 200

            if size_f_t == 'f':
                new_height = fixed_full_height
            elif size_f_t == 't':
                new_height = fixed_thumbnail_height
            else:
                pass
            try:
                image = Image.open(image_path)
                width = image.width
                height = image.height
                filename = image.filename
                new_name = filename.split('.')
                file_name = new_name[0].split('\\')[-1]
                file_name_filled_space = file_name.replace(' ', '-')
                # new_filename = file_name_filled_space + '.jpg'
                # extension = new_filename.pop()

                if size_f_t == 'f':
                    new_filename = f"{file_name_filled_space}-f.jpg"
                    output_filepath = output_folder + new_filename
                elif size_f_t == 't':
                    new_filename = f"{file_name_filled_space}-t.jpg"
                    output_filepath = output_folder + new_filename

                ratio = (new_height / float(height))
                new_width = int(float(width * ratio))

                image = image.resize((new_width, new_height))
                image = image.convert('RGB')
                if not os.path.exists(output_folder):
                    os.mkdir(output_folder)
                image.save(output_filepath)

            except Exception as e:
                pass
        else:
            pass


def generate_captcha():
    captcha_num = str(random.randrange(100000, 999999))
    img = ImageCaptcha()
    captcha_io = img.generate(captcha_num)
    binary_data = captcha_io.getvalue()
    encoded_data_bytes = base64.b64encode(binary_data)
    encoded_string = encoded_data_bytes.decode('utf-8')
    captcha_uri = f"data:image/png;base64, {encoded_string}"
    return captcha_num, captcha_uri


def calculate_age(birthdate):
    year, month, day = map(int, birthdate.split("-"))
    today = date.today()
    print(today)
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

def uuid_generator(table_name):
    uuid_list = []

    result = db.session.query(eval(table_name)).all()
    print(result)
    for row in result:
        uuid_list.append(row.uuid)
    unique = False
    uuid = ''
    while not unique:
        u = random.randint(100000, 999999)
        if u not in uuid_list:
            uuid = u
            unique = True
    return uuid