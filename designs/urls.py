from django.urls import path
from .views import DesignList, DesignDetailView, add_comment, DesignCreateView, CommentCreateView, get_comments

app_name = 'designs'
urlpatterns = [
    path('', DesignList.as_view(), name='design_list'),
    path('new/', DesignCreateView.as_view(), name='design_create'),
    path('<int:pk>/', DesignDetailView.as_view(), name='design_detail'),
    path('comment/<int:design_id>/', CommentCreateView.as_view(), name='add_comment'),
    path('api/design/<int:design_id>/comments/', get_comments, name='get_comments'),

]
