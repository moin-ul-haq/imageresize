from .services import resize_image
from celery import shared_task
from time import sleep


@shared_task
def perform_operation(image_path):
    sleep(50)
    return resize_image(image_path)