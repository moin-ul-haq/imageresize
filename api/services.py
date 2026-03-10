import os
from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image

def save_uploaded_image(file):
    uploaded_path=os.path.join('uploads',file.name)
    file_path=default_storage.save(uploaded_path,file)
    full_path=os.path.join(settings.MEDIA_ROOT,file_path)

    return full_path 


def resize_image(image_path):
    img=Image.open(image_path)
    img=img.resize([500,500])

    filename=os.path.basename(image_path)
    processed_dir=os.path.join(settings.MEDIA_ROOT,'processed')

    os.makedirs(processed_dir,exist_ok=True)
    processed_path=os.path.join(processed_dir,filename)

    img.save(processed_path)

    return processed_path