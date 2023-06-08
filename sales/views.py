from django.shortcuts import render, redirect
from .models import Product, Review, Order
from .forms import ProductForm, ReviewForm, OrderForm
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


def add_to_cart(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    if product_pk in cart:
        cart[product_pk]['quantity'] += quantity
    else:
        cart[product_pk] = {'quantity': quantity, 'price': str(product.price), 'product_pk': product.pk}

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



def payment(request):
    return render(request, 'sales/payment.html')

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # 장바구니에 담긴 정보 가져오기
            cart_items = request.POST.getlist('product[]')
            quantities = request.POST.getlist('quantity[]')
            total_price = request.POST.get('total_price')
            customer = request.POST.get('customer')
            
            # 주문 정보 생성
            for i in range(len(cart_items)):
                product_name = cart_items[i]
                quantity = int(quantities[i])
                price = total_price
                
                # 주문 정보 저장
                order = form.save(commit=False)
                order.user_id = customer
                order.product_name = product_name
                order.quantity = quantity
                order.price = price
                order.save()
                # 주문 정보 처리 (예: 결제 등)
                # ...
            
            # 주문 완료 후 장바구니 비우기
            # ...
            
            return redirect('sales:order_complete')
    else:
        form = OrderForm()
    context ={
        'form': form,
    }

    return render(request, 'sales/create_order.html', context)

def order_complete(request):
    order_id = request.GET.get('order_id', None)
    if order_id is not None:
        order = Order.objects.get(id=order_id)
        context = {'order': order}
        return render(request, 'sales/order_complete.html', context)
    else:
        return render(request, 'sales/order_complete.html')
    