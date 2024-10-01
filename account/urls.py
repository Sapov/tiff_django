from django.urls import path
from . import views
from .views import politics

app_name = 'account'

urlpatterns = [
    # ----------profile--------------
    path('edit/', views.edit_profile, name='edit_profile'),
    path('list_profile/', views.ListProfile.as_view(), name='list_profile'),
    path('politics/', politics, name='politics'),

    # -------------------------CRUD ORGANISATION-----------------------------------------------
    path('add_organisation/', views.OrganisationCreateView.as_view(), name='create_organisation'),
    # path('add_organisation_test/', OrganisationCreateViewTest.as_view(), name='add_organisation_test'),
    path('list_organisation/', views.ListOrganisation.as_view(), name='list_organisation'),
    path('delete_organisation_user/<pk>', views.OrganisationDeleteView.as_view(), name='delete_organisation_user'),
    path('update_organisation_user/<pk>', views.OrganisationUpdateView.as_view(), name='update_organisation_user'),

    path('', views.dashboard, name='dashboard'),

    # ---------------------------- CRUD ADDRESS delivery user ---------------------------
    path('delivery_list/', views.DeliveryAddressListView.as_view(), name='delivery_list'),
    path('delivery_create/', views.DeliveryAddressCreateView.as_view(), name='delivery_create'),
    path('delivery_update/<pk>', views.DeliveryAddressUpdate.as_view(), name='delivery_update'),
    path('delivery_delete/<pk>', views.DeliveryAddressDelete.as_view(), name='delivery_delete'),

]

