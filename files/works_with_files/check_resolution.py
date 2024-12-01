from files.models import Product


class CheckResolution:
    ''' Сравниваем разрешение загруженного файла и стандартное разрешение
     для печати'''
    def __init__(self, file_id: int):
        self.file_id = file_id

    def checking(self):
        files = Product.objects.get(id=self.file_id)
        print(f'Разрешение файла {files.resolution} VS Разрешение печати {files.material.resolution_print}')
        if files.resolution < files.material.resolution_print:
            print(f"Разрешение файла {files.resolution} меньше положенного {files.material.resolution_print}")
            return f"Разрешение файла {files.resolution} меньше положенного {files.material.resolution_print}"

            print('Ширина', files.width)
            print('le', files.length)
            print('res', files.resolution)
            print('Material', files.material)
            print('Name', files.material.name)
            print('ResPrint', files.material.resolution_print)


# if __name__ == "__main__":
