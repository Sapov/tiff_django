from django.urls import path
from .views import (DesignList, DesignDetailView, add_comment, DesignCreateView, CommentCreateView, get_comments,
                    add_desing_in_work)

app_name = 'designs'
urlpatterns = [
    path('', DesignList.as_view(), name='design_list'),
    path('new/', DesignCreateView.as_view(), name='design_create'),
    path('<int:pk>/', DesignDetailView.as_view(), name='design_detail'),
    path('comment/<int:design_id>/', CommentCreateView.as_view(), name='add_comment'),
    path('api/design/<int:design_id>/comments/', get_comments, name='get_comments'),
    path('design/<int:design_id>/add_comment/', add_comment, name='add_comment'),
    path('design_in_work/<int:design_id>/', add_desing_in_work, name='add_desing_in_work'),

    # path('design/<int:design_id>/comments/', get_comments, name='get_comments'),

]
