from django.urls import path
from django.views.generic import TemplateView, DetailView

from main import models
from .views import ContactUsView, ProductListView, OrdersView, AccountInformationView, add_to_basket, manage_basket, AllProductsListView, AddressSelectionView, room


urlpatterns = [
        path('', TemplateView.as_view(template_name='main/home.html'), name='home'),
        path('about-us/', TemplateView.as_view(template_name='main/about_us.html'), name = 'about_us'),
        path('contact-us/', ContactUsView.as_view(), name = 'contact_us'),
        path('account-information/', AccountInformationView.as_view(), name = 'account_information'),

        path('products/', AllProductsListView.as_view(), name = 'all_products'),
        path('products/<slug:slug>/', DetailView.as_view(model = models.Product), name = 'product'),
        path('products/tags/<slug:tag>/', ProductListView.as_view(), name = 'product_tags_list'),

        path('add-to-basket/', add_to_basket, name = 'add_to_basket'),
        path('basket/', manage_basket, name = 'basket'),

        path('orders/', OrdersView.as_view(), name = "all_orders"),
        path('order/done/', TemplateView.as_view(template_name = "main/order_done.html"), name = "checkout_done"),
        path('order/address_select/', AddressSelectionView.as_view(), name = "address_select"),

        path("customer-service/<int:order_id>/", room, name = "cs_chat"),
        path("customer-service/", TemplateView.as_view(template_name = "customer_service.html"), name = "cs_main"),
]
