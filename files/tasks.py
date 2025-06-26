import os

from celery import shared_task

from files.models import FileUpload
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
        # time.sleep(0.1)  # Замените на реальную обработку
        progress_recorder.set_progress(i + 1, 100, description='Обработка файла')

    return {'result': 'success'}




@shared_task(bind=True)
def process_large_file(self, upload_id):
    upload = FileUpload.objects.get(id=upload_id)
    upload.status = 'processing'
    upload.task_id = self.request.id
    upload.save()

    try:
        file_path = upload.file.path
        file_size = os.path.getsize(file_path)
        chunk_size = 1024 * 1024  # 1MB

        # Имитация обработки с обновлением прогресса
        with open(file_path, 'rb') as f:
            processed = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                # Здесь ваша обработка чанка
                # time.sleep(0.1)  # Имитация работы

                processed += len(chunk)
                progress = int((processed / file_size) * 100)
                self.update_state(state='PROGRESS', meta={'progress': progress})

                upload.progress = progress
                upload.save()

        upload.status = 'completed'
        upload.result = {'message': 'File processed successfully'}
        upload.save()
        return {'status': 'completed', 'result': upload.result}

    except Exception as e:
        upload.status = 'failed'
        upload.result = {'error': str(e)}
        upload.save()
        raise self.retry(exc=e, countdown=60)