from django.urls import path
from .views import AddressListView, AddressCreateView, AddressDeleteView, AddressUpdateView

urlpatterns = [
        path('', AddressListView.as_view(), name = "address_list"),
        path('create/', AddressCreateView.as_view(), name = "address_create"),
        path('<int:pk>', AddressUpdateView.as_view(), name = "address_update"),
        path('<int:pk>/delete/', AddressDeleteView.as_view(), name = "address_delete"),
]
