from django.urls import path
from .views import DesignLIst, DesignDetailView, add_comment

app_name = 'designs'
urlpatterns = [
    path('', DesignLIst.as_view(), name='design_list'),
    # path('category/<slug:category_slug>/', ArticleListView.as_view(), name='article_list_by_category'),
    # path('new/', DesignCreateView.as_view(), name='design_create'),
    path('<int:pk>/', DesignDetailView.as_view(), name='design_detail'),
    # path('article/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    # path('article/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('comments/<int:id>/', add_comment, name='add_comment'),

]
