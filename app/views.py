from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate

from app.models import Product, Category, Cart, CartItem, Order
from app.forms import OrderForm, RegistrationForm, LoginForm
from django.contrib.auth.models import User


def main_view(request):
    context = {}
    context['phones'] = Product.objects.filter(category__title='phones')
    context['other'] = Product.objects.filter(category__title='other')
    context['categories'] = Category.objects.all()
    return render(request, 'app/index.html', context)


# Product views

def product_detail(request, *args, **kwargs):
    context = {}
    slug = kwargs['slug']
    context['product'] = get_object_or_404(Product, slug=slug)
    context['categories'] = Category.objects.all()
    return render(request, 'app/product_detail.html', context)


def products_of_category_view(request, *args, **kwargs):
    slug = kwargs['slug']

    context = {}
    context['products'] = Product.objects.filter(category__title__iexact=slug)
    context['categories'] = Category.objects.all()
    return render(request, 'app/products_of_category.html', context)


# Cart views

def cart_session(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(pk=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart


def cart_view(request):
    context = {}
    context['cart'] = cart_session(request)
    context['categories'] = Category.objects.all()
    return render(request, 'app/cart.html', context)


def add_to_cart_view(request):
    slug = request.GET.get('slug')
    cart = cart_session(request)
    product = Product.objects.get(slug=slug)
    cart.add_to_cart(product)

    cart.count_cart_total()
    return JsonResponse({})


def remove_from_cart_view(request):
    slug = request.GET.get('slug')
    cart = cart_session(request)
    product = Product.objects.get(slug=slug)
    cart.remove_from_cart(product)

    cart_total = cart.count_cart_total()
    return JsonResponse({'cart_total': cart_total})


def change_item_quantity_view(request):
    context = {}
    cart = cart_session(request)
    context['cart'] = cart
    quantity = int(request.GET.get('quantity', 1))
    item_id = int(request.GET.get('item_id', 1))

    cart_item = CartItem.objects.get(pk=item_id)
    cart_item.change_quantity(quantity)

    cart_total = cart.count_cart_total()

    return JsonResponse({'item_total': cart_item.item_total,
                         'cart_total': cart_total})


def checkout_view(request):
    context = {}
    context['cart'] = cart_session(request)
    context['categories'] = Category.objects.all()
    return render(request, 'app/checkout.html', context)


def order_create_view(request):
    context = {}
    form = OrderForm(request.POST or None)
    context['form'] = OrderForm(request.POST or None)
    cart = cart_session(request)
    context['cart'] = cart

    if form.is_valid():
        new_order = Order()
        new_order.user = request.user
        new_order.save()
        new_order.items.add(cart)
        new_order.first_name = form.cleaned_data['first_name']
        new_order.last_name = form.cleaned_data['last_name']
        new_order.phone = form.cleaned_data['phone']
        new_order.buying_type = form.cleaned_data['buying_type']
        new_order.address = form.cleaned_data['address']
        new_order.comment = form.cleaned_data['comment']
        new_order.total = cart.cart_total
        new_order.save()

        del request.session['cart_id']
        return HttpResponseRedirect(reverse('congratulations'))
    return render(request, 'app/order.html', context)


def congratulations_view(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request, 'app/congratulations.html', context)


def empty_section(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request, 'app/empty_section.html', context)


# Accounts views

def account_view(request):
    context = {}
    try:
        context['orders'] = Order.objects.filter(user=request.user).order_by('-pk')
    except:
        context['orders'] = None
    context['categories'] = Category.objects.all()
    return render(request, 'app/account.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    context = {}
    context['form'] = form
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        new_user.username = username
        new_user.password = password
        new_user.first_name = form.cleaned_data['first_name']
        new_user.last_name = form.cleaned_data['last_name']
        new_user.email = form.cleaned_data['email']
        new_user.save()

        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('main_page'))
        return HttpResponseRedirect(reverse('main_page'))

    context['categories'] = Category.objects.all()
    return render(request, 'app/registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    context = {}
    context['form'] = form

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        username = User.objects.get(email=email).username

        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('main_page'))

    context['categories'] = Category.objects.all()
    return render(request, 'app/login.html', context)
