from celery import shared_task
from files.works_with_files.image_tiff_file import ImageFile
from celery_progress.backend import ProgressRecorder
import time

@shared_task
def resize_image(file):
    item_file = ImageFile(file.image)
    item_file.resolution_reduction(file.material.resolution_print)


@shared_task(bind=True)
def process_uploaded_file(self, file_path, user_id):
    progress_recorder = ProgressRecorder(self)

    # Имитация обработки файла
    for i in range(100):
        time.sleep(0.1)  # Замените на реальную обработку
        progress_recorder.set_progress(i + 1, 100, description='Обработка файла')

    return {'result': 'success'}
