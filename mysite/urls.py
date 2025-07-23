from django.contrib import admin
from django.templatetags.static import static
from django.urls import path, include, re_path

from django.conf.urls.static import static
from django.conf import settings

from files.views import page_not_found, MaterialViewSet

from rest_framework import routers
from files.api_view import FilesViewSet

router = routers.SimpleRouter()
router.register(r'materials', FilesViewSet)

from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

handler404 = page_not_found
urlpatterns = [
                  path("files/", include("files.urls")),
                  path("", include("users.urls")),
                  path('', include('django.contrib.auth.urls')),
                  path("account/", include("account.urls")),
                  path("lids/", include("lids.urls")),
                  path("orders/", include("orders.urls")),
                  path("info/", include("info.urls")),
                  path("kbase/", include("kbase.urls")),
                  path("designs/", include("designs.urls")),
                  path("delivery_in_bus/", include("delivery_in_bus.urls")),
                  path("admin/", admin.site.urls),
                  path('celery-progress/', include('celery_progress.urls')),

                  path("api/v1/", include(router.urls)),  # api/v1/material

                  re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# # включаем возможность обработки картинок
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]
