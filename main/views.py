from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render

from django.views.generic.edit import FormView
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .models import Product, ProductTag, ProductImage, Basket, BasketLine, Order
from main.forms import BasketLineFormSet, AddressSelectionForm, ContactForm

class AccountInformationView(TemplateView):
    template_name = "main/account_information.html"


class ContactUsView(FormView):
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)

class AllProductsListView(ListView):
    model = Product
    template_name = 'main/all_products_name.html'
    queryset = Product.objects.active()

class ProductListView(ListView):
    template_name = "main/product_list.html"
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != "all":
            self.tag = get_object_or_404(ProductTag, slug = tag)
        if self.tag:
            products = Product.objects.active().filter(tags = self.tag)
        else:
            products = Product.objects.active()

        return products.order_by("name")

def add_to_basket(request):
    product = get_object_or_404(
        Product, pk=request.GET.get("product_id")
    )
    basket = request.basket
    if not request.basket:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        basket = Basket.objects.create(user=user)
        request.session["basket_id"] = basket.id

    basketline, created = BasketLine.objects.get_or_create(
        basket=basket, product=product
    )
    if not created:
        basketline.quantity += 1
        basketline.save()
    return HttpResponseRedirect(
        reverse("product", args=(product.slug,))
    )


def manage_basket(request):
    if not request.basket:
        return render(request, "main/basket.html", {"formset": None})

    if request.method == "POST":
        formset = BasketLineFormSet(
            request.POST, instance=request.basket
        )
        if formset.is_valid():
            formset.save()
    else:
        formset = BasketLineFormSet(
            instance=request.basket
        )

    if request.basket.is_empty():
        return render(request, "main/basket.html", {"formset": None})

    return render(request, "main/basket.html", {"formset": formset})

class AddressSelectionView(LoginRequiredMixin, FormView):
    template_name = "main/address_select.html"
    form_class = AddressSelectionForm
    success_url = reverse_lazy('checkout_done')

    #To pass the user in the form(to have access to its own address)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        del self.request.session['basket_id']
        basket = self.request.basket
        basket.create_order(
            form.cleaned_data['billing_address'],
            form.cleaned_data['shipping_address']
        )
        return super().form_valid(form)


def room(request, order_id):
    return render(request, "chat_room.html", {"room_name_json": str(order_id)},)

class OrdersView(LoginRequiredMixin, ListView):
    template_name = "main/orders.html"

    def get_queryset(self):
        orders = Order.objects.filter(user = self.request.user)
        return orders
