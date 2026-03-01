from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from profiles.views import edit_profile
from users.views import Register, EmailVerify, MyLoginView, UserListsView, UsersCreateView, UserUpdateLIst, \
    UserDeleteView, ListProfile, ProfileUpdateLIst, DesignerSignUpView

# app_name = "users"

urlpatterns = [

    # ---------------CRUD--USERS----------------
    path('users_lists/', UserListsView.as_view(), name='users_list'),
    path('users_create/', UsersCreateView.as_view(), name='users_create'),
    path('users_update/<int:pk>', UserUpdateLIst.as_view(), name='users_update'),
    path('users_delete/<int:pk>', UserDeleteView.as_view(), name='users_delete'),
    # --------------CRUD PROFILE------------
    path('profile_list/', ListProfile.as_view(), name='list_profile'),
    path('profile_edit/', edit_profile, name='profile_edit'),

    path('signup/designer/', DesignerSignUpView.as_view(), name='designer_signup'),

]
