from django.urls import path
from .views import sale_banner, SiteOrderCreateView, order_complete

app_name = 'bforms'

urlpatterns = [
    path('sale_banner/', sale_banner, name='sale_banner'),
    path('site_order/', SiteOrderCreateView.as_view(), name='site_order'),
    path('order_complete/', order_complete, name='order_complete'),

]

