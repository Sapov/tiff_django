from django.urls import path

from django.contrib.auth import views as auth_views
from . import views
from .views import *

app_name = "info"

urlpatterns = [
    path("", banner, name="ba"),
    path("banner/", index, name="banindex"),
    path("feedback/", feedback, name="feedback"),
    # ----------profile--------------
    # -------------------------CRUD ORGANISATION-----------------------------------------------
    # path('list_organisation/', views.ListOrganisation.as_view(), name='list_organisation'),
    # path('delete_organisation_user/<pk>', views.OrganisationDeleteView.as_view(), name='delete_organisation_user'),
    # path('update_organisation_user/<pk>', views.OrganisationUpdateView.as_view(), name='update_organisation_user'),
]
