from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.forms import UserCreationForm

from .models import User
#
# User = get_user_model()
#
#
# @admin.register(User)
# class UserAdmin(UserAdmin):
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'Role'),
#         }),
#     )
#
#     add_form = UserCreationForm
#

# admin.site.register(User)
admin.site.register(User)
