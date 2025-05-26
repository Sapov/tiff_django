from django.urls import path
from .views import *

app_name = 'design'
urlpatterns = [
    path('', DesignViewList.as_view(), name='design_list'),
    # path('category/<slug:category_slug>/', ArticleListView.as_view(), name='article_list_by_category'),
    # path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    path('<slug:slug>/', DesignDetailView.as_view(), name='design_detail'),
    # path('article/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    # path('article/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
