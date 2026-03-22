from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from files.models import Product, Material, FinishWork, StatusProduct


class BannerGeneratorView(View):
    """View для генерации и сохранения баннеров"""

    def get(self, request):
        """
        Отображает страницу генератора баннеров.
        """
        context = {
            'title': 'Заказать баннер "ПРОДАЮ"',
            'page_name': 'banner_generator',
        }

        return render(request, 'files/create_banner.html', context)


@csrf_exempt
def submit_banner_order(request):
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            user = request.user
            text = request.POST.get('text')
            phone = request.POST.get('phone')
            bg_color = request.POST.get('bg_color')
            text_color = request.POST.get('text_color')
            grommet_type = request.POST.get('grommet_type')
            price_banner = request.POST.get('total_cost')

            # Получаем изображение из canvas
            canvas_image = request.FILES.get('canvas_image')

            if canvas_image:
                material = Material.objects.get(id=1)
                finish_work = FinishWork.objects.get(id=1)
                status = StatusProduct.objects.get(id=1)
                print(f"Material {material},'\n',"
                      f"finish_work {finish_work},'\n'"
                      f"status {status}'\n'"
                      f"user {request.user}\n"
                      f" canvas_image {canvas_image}\n"
                      f"")

                try:
                    Product.objects.create(
                    user=request.user,
                    material = material,
                    quantity = 1,
                    width = 1,#request.POST.get('width'),
                    length = 1,#request.POST.get('length'),
                    # resolution = 0,
                    color_model =  "CMYK",
                    size = 0,
                    price = 0,
                    cost_price = 0,
                    images = canvas_image,
                    FinishWork = finish_work,
                    status_product = status,
                    comments = '',
                    )
                except Exception as e:
                    print(e)
                    print(f"Тип ошибки: {type(e).__name__}")
                    print(f"Сообщение: {str(e)}")
                    print(f"Полная информация: {e}")



                return JsonResponse({
                    'status': 'success',
                    'message': 'Заказ принят в обработку',
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Изображение не получено'
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Неверный метод запроса'
    }, status=405)


def delivery(request):
    # https://yandex.ru/support/delivery-profile/ru/modules/widgets#widget-setup
    return render(request, 'orders/delivery.html')
