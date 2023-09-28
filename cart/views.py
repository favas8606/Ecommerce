from django.shortcuts import get_object_or_404, render, redirect
from ecommerce_app . models import Products
from . models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart
def add(request, product_id):
    product = Products.objects.get(id = product_id)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product= product, cart = cart)
        # check whether item is out of stock or not
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product = product, quantity = 1, cart = cart)

    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_item=None):

    try:
        cart = Cart.objects.get(cart_id =_cart_id(request))
        cart_item = CartItem.objects.filter(cart=cart, active=True)
        for _item in cart_item:
            total += (_item.product.price * _item.quantity)
            counter += _item.quantity
    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html', dict(cart_item=cart_item, total=total, counter=counter))


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Products, id=product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    try:

        if cart_item.quantity >= 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    
    return redirect('cart:cart_detail')


def delete_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Products, id= product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    
    return redirect('cart:cart_detail')
