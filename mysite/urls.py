"""printbanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.templatetags.static import static
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from files.views import page_not_found

urlpatterns = [
    path("users/", include("users.urls")),
    path("", include("files.urls")),
    path("account/", include("account.urls")),
    path("orders/", include("orders.urls")),
    path("info/", include("info.urls")),
    path("admin/", admin.site.urls),
]

handler404 = page_not_found

#
# # включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
