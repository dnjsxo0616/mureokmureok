from django.shortcuts import render, redirect
from .models import Product, Purchase, Review
from .forms import ProductForm, ReviewForm
# from .forms import PurchaseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.models import User, User_title, User_profile
from django.db.models import Count, Q
from django.http import JsonResponse
from decimal import Decimal

def index(request):
    # 베스트 프로덕트(리뷰순)
    products = Product.objects.all()

    context = {
        'products': products,
        'room_name': "broadcast"
    }

    return render(request, 'sales/index.html', context)



@login_required
def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('sales:index')
    else:
        form = ProductForm()
    
    context = {
        'form' : form,
        'room_name': "broadcast"
    }
    return render(request, 'sales/create.html', context)



def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    # products = Product.objects.all().order_by('like')

    context ={
        'product' : product,
        # 'products': products,
        'room_name': "broadcast"
    }
    return render(request,'sales/detail.html', context)


def delete_review(request, product_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    review.delete()
    return redirect('sales:detail', product_pk)



@login_required
def update_review(request, product_pk, review_pk):
    product = Product.objects.get(pk=product_pk)
    review = Review.objects.get(pk=review_pk)
    
    if request.user != review.user:
        return redirect('sales:detail', product_pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('sales:detail', product_pk)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'product': product,
        'review': review,
        'form': form,
        'room_name': "broadcast"
    }
    return render(request, 'sales/detail.html', context)


# def delete(request, product_pk):
#     product = Product.objects.get(pk=product_pk)
#     if request.user == product.user:
#         product.delete()
#     return redirect('sales:index')



# def update(request):
#     product = Product.objects.get(pk=product_pk)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('sales:detail', product.pk)
#     else:
#         form = ProductForm(instance=product)
#     context = {
#         'product':product,
#         'form' : form,
#     }
#     return render(request,'sales/update.html',context)



# def purchase_list(request, pk):
#     products = Product.objects.all()
#     user = User.objects.get(pk=pk)
#     purchases = Purchase.objects.filter(user=user)
#     paginator = Paginator(orders, 5)
#     page = request.GET.get('page')
#     context = {
#         'user': user, 
#         'purchases': purchases, 
#         'products': products
#     }
#     return render(request, 'sales/purchase_list.html', context)



def add_to_cart(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})

    if product_pk in cart:
        cart[product_pk]['quantity'] += quantity
    else:
        cart[product_pk] = {'quantity': quantity, 'price': str(product.price)}

    request.session['cart'] = cart

    return redirect('sales:cart')


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for product_pk, product_info in cart.items():
        product = Product.objects.get(pk=product_pk)
        
        total_price = Decimal(product_info['quantity']) * product.price
        cart_total += total_price
        cart_items.append({
            'product': product,
            'quantity': product_info['quantity'],
            'total_price': total_price,
        })

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'room_name': "broadcast"

    }
    return render(request, 'sales/cart.html', context)


def remove_from_cart(request, product_pk):
    cart = request.session.get('cart', {})
    product_pk = str(product_pk)

    if product_pk in cart:
        del cart[product_pk]
        request.session['cart'] = cart


    return redirect('sales:cart')

@login_required 
def create_review(request, product_pk):
    product = Product.objects.get(pk = product_pk)
    form = ReviewForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('sales:detail', product_pk)
    context = {
        'product':product,
        'form':form,
        'room_name': "broadcast"
    }
    return render(request, 'sales/detail.html', context)


# def cart(request, pk):
#     user = User.objects.get(pk=pk)
#     cart = Cart.objects.filter(user=user)
#     paginator = Paginator(cart, 10)

#     context = {
#         'user': user, 
#         'cart': cart
#     }
#     return render(request, 'sales/cart.html', context)





# def delete_cart(request, pk):
#     user = request.user
#     cart = Cart.objects.filter(user=user)
#     quantity = 0

#     if request.method == 'POST':
#         pk = int(request.POST.get('product'))
#         product = Product.objects.get(pk=pk)
#         for i in cart:
#             if i.products == product :
#                 quantity =  i.quantity

#         if quantity > 0 :
#             product = Product.objects.filter(pk=pk)
#             cart = Cart.objects.filter(user=user, products__in=product)
#             cart.delete()
#             return redirect('shop:cart', user.pk)



def payment(request):
    return render(request, 'sales/payment.html')