from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from app.views import (main_view,
                       cart_view,
                       empty_section,
                       products_of_category_view,
                       product_detail,
                       add_to_cart_view,
                       remove_from_cart_view,
                       change_item_quantity_view,
                       checkout_view,
                       order_create_view,
                       congratulations_view,
                       account_view,
                       registration_view,
                       login_view)

urlpatterns = [
    path('', main_view, name='main_page'),
    path('category/<str:slug>/', products_of_category_view, name='category'),
    path('product/<str:slug>/', product_detail, name='product'),
    path('cart/', cart_view, name='cart'),
    path('cart/remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('cart/change_item_quantity/', change_item_quantity_view, name='change_item_quantity'),
    path('cart/add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('cart/checkout/', checkout_view, name='checkout'),
    path('cart/order/', order_create_view, name='order_create'),
    path('cart/congratulations/', congratulations_view, name='congratulations'),
    path('account/', account_view, name='account'),
    path('account/login/', login_view, name='login'),
    path('account/registration/', registration_view, name='registration'),
    path('account/logout/', LogoutView.as_view(next_page=reverse_lazy('main_page')), name='logout'),
    path('empty_section/', empty_section, name='empty_section'),
]
