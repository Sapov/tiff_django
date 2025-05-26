from django.urls import path

from .views import CreteDesignOrder, DesignDetailView, add_comment, ListViewDesign

app_name = 'design'

urlpatterns = [
    path('', ListViewDesign.as_view(), name='list_design'),
    path('new/', CreteDesignOrder.as_view(), name='order_design_create'),
    path('<pk>/', DesignDetailView.as_view(), name='detail_design'),
    # path('category/<slug:category_slug>/', ArticleListView.as_view(), name='article_list_by_category'),
    # path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    # path('article/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    # path('article/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('/<pk>/comment/', add_comment, name='add_comment'),
]
