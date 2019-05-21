from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from app.models import Product, Category, Cart, CartItem, Order
from app.forms import OrderForm

def main(request):
    context = {}
    context['phones'] = Product.objects.filter(category__title='phones')
    context['other'] = Product.objects.filter(category__title='other')
    context['categories'] = Category.objects.all()
    return render(request, 'app/index.html', context)

def products_of_category(request, *args, **kwargs):
    slug = kwargs['slug']

    context = {}
    context['products'] = Product.objects.filter(category__title__iexact=slug)
    context['categories'] = Category.objects.all()
    return render(request, 'app/products_of_category.html', context)


class Categories(DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        if self.kwargs:
            id = self.kwargs['id']
            context['products'] = Product.objects.get(pk=id)

        return context

    def get_queryset(self, *args, **kwargs):
        category = self.kwargs['category']
        return Category.objects.filter(title=category)


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


#

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

def checkout_view(request):
    context = {}
    context['cart'] = cart_session(request)
    context['categories'] = Category.objects.all()
    return render(request, 'app/checkout.html', context)

def empty_section(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request, 'app/empty_section.html', context)

def login(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request, 'app/login.html', context)

def product_detail(request, *args, **kwargs):
    context = {}
    slug = kwargs['slug']
    context['product'] = get_object_or_404(Product, slug=slug)
    return render(request, 'app/product_detail.html', context)

class ProductView(DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        if self.kwargs:
            product_id = int(kwargs['id'])
            context['phone'] = get_object_or_404(Product, id=product_id)
            # return render(self.request, 'app/phone.html', {'phone': phone})

            # if product_id in self.request.session.get('reviewed_products', []):
            #     context['is_review_exist'] = True
        return context

    def get_queryset(self):
        return Product.objects.all()

    # def post(self, request, *args, **kwargs):
    #     product_id = int(self.kwargs['pk'])
    #     form = ReviewForm(self.request.POST)
    #
    #     if form.is_valid():
    #         review = form.save(commit=False)
    #         review.product_id = product_id
    #         review.save()
    #         self.request.session['reviewed_products'] = self.request.session.get('reviewed_products', []) + [product_id]
    #
    #     return redirect(reverse('product_detail', kwargs={'pk': product_id}))

def phone(request, **kwargs):
    product_id = int(kwargs['id'])
    phone = get_object_or_404(Product, id=product_id)
    return render(request, 'app/phone.html', {'phone': phone})

def smartphones(request):
    context = {}
    context['smartphones'] = Product.objects.filter(category__title='phone')
    return render(request, 'app/smartphones.html', context)

class ProductsList(ListView):
    model = Product
    context_object_name = 'product_list'

# Create your views here.
class ProductView(DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        if self.kwargs:
            product_id = int(self.kwargs['id'])
            context['object'] = Product.objects.get(id=product_id)
            context['price'] = Product.objects.get(product_id=product_id)
            # context['form'] = ReviewForm

            # if product_id in self.request.session.get('reviewed_products', []):
            #     context['is_review_exist'] = True

        return context

    def get_queryset(self):
        return Product.objects.all()

    # def post(self, request, *args, **kwargs):
    #     product_id = int(self.kwargs['pk'])
    #     form = ReviewForm(self.request.POST)

    #     if form.is_valid():
    #         review = form.save(commit=False)
    #         review.product_id = product_id
    #         review.save()
    #         self.request.session['reviewed_products'] = self.request.session.get('reviewed_products', []) + [product_id]

    #     return redirect(reverse('product_detail', kwargs={'pk': product_id}))