from django.urls import path
from .views import *

urlpatterns = [
    path('', DesignVewList.as_view(), name='desing_list'),
    # path('category/<slug:category_slug>/', ArticleListView.as_view(), name='article_list_by_category'),
    # path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    # path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    # path('article/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    # path('article/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
