from django.urls import path
from .views import DesignDetailView

urlpatterns = [
    path('', DesignDetailView.as_view(), name='detail_order'),
    # path('category/<slug:category_slug>/', ArticleListView.as_view(), name='article_list_by_category'),
    # path('article/new/', ArticleCreateView.as_view(), name='article_create'),
    # path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    # path('article/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    # path('article/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    # path('article/<slug:slug>/comment/', add_comment, name='add_comment'),
]
