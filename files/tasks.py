from celery import shared_task

from files.works_with_files.image_tiff_file import ImageFile


@shared_task
def resize_image(file):
    item_file = ImageFile(file.image)
    item_file.resolution_reduction(file.material.resolution_print)


if __name__ == "__main__":
    main()
