from django.urls import path
from .views import *

app_name = 'designs'
urlpatterns = [
    # path('', DesignViewList.as_view(), name='design_list'),
    # path('category/<slug:category_slug>/', ArticleListView.as_view(), name='article_list_by_category'),
    # path('new/', DesignCreateView.as_view(), name='design_create'),
    # path('<slug:slug>/', get_comment_in_order, name='design_detail'),
    # path('article/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    # path('article/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
