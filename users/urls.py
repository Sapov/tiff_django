from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from account.views import edit_profile
from users.views import Register, EmailVerify, MyLoginView, UserListsView, UsersCreateView, UserUpdateLIst, \
    UserDeleteView, ListProfile, ProfileUpdateLIst

# app_name = "users"

urlpatterns = [

    path('', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('', include('django.contrib.auth.urls')),

    path('invalid_verify/', TemplateView.as_view(template_name='registration/invalid_verify.html'),
         name='invalid_verify'),

    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),

    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'),
         name='confirm_email'),
    path('register/', Register.as_view(), name='register'),
    # ---------------CRUD--USERS----------------
    path('users_lists/', UserListsView.as_view(), name='users_list'),
    path('users_create/', UsersCreateView.as_view(), name='users_create'),
    path('users_update/<int:pk>', UserUpdateLIst.as_view(), name='users_update'),
    path('users_delete/<int:pk>', UserDeleteView.as_view(), name='users_delete'),
    # --------------CRUD PROFILE------------
    path('profile_list/', ListProfile.as_view(), name='profile_list'),
    path('profile_edit/', edit_profile, name='profile_edit'),

]
