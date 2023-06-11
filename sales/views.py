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
from django.core import serializers
from django.views.generic import ListView


def index(request):
    # 베스트 프로덕트(리뷰순)
    products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'page_obj': page_obj,
        'room_name': "broadcast",
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
            return redirect('sales:detail', product.pk)
    else:
        form = ProductForm()
    
    context = {
        'form' : form,
        'room_name': "broadcast"
    }
    return render(request, 'sales/create.html', context)


@login_required
def like(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if product.like_users.filter(pk=request.user.pk).exists():
        product.like_users.remove(request.user)
        is_liked = False
    else:
        product.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'like_count': product.like_users.count(),
    }
    return JsonResponse(context)


def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    reviews = product.reviews.all()
    # products = Product.objects.all().order_by('like')

    if request.method =='POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.score = request.POST.get('score')
            review.save()
    else:
        review_form = ReviewForm()
    context ={
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'room_name': "broadcast"
    }
    return render(request,'sales/detail.html', context)


def filter(request):
    category = request.GET.getlist('category')
    low_price = request.GET.get('low_price', 0)
    high_price = request.GET.get('high_price', None)

    if low_price:
        low_price = int(low_price)
    if high_price:
        high_price = int(high_price)

    if category:
        products = Product.objects.filter(category__in=category)
    else:
        products = Product.objects.all()

    if low_price or high_price:
        price_filter = Q()
        if low_price:
            price_filter &= Q(price__gte=low_price)
        if high_price:
            price_filter &= Q(price__lte=high_price)
        products = products.filter(price_filter).distinct()

    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'category': category,
        'low_price': low_price,
        'high_price': high_price,
        'page_obj': page_obj,
        'room_name': "broadcast",
    }
    return render(request, 'sales/filter.html', context)


def sort(request, *args, **kwargs):
    sort_type = request.GET.get('sort_type')
    queryset = super().get_queryset()

    if sort_type == 'popularity':
        queryset = queryset.order_by('-views')
    elif sort_type == 'latest':
        queryset = queryset.order_by('-created_at')
    elif sort_type == 'price_low':
        queryset = queryset.order_by('price')
    elif sort_type == 'price_high':
        queryset = queryset.order_by('-price')

    data = serializers.serialize('json', queryset)

    paginator = Paginator(data, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'room_name': "broadcast",
    }
    return JsonResponse(context, safe=False)


@login_required
def update(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('sales:detail', product.pk)
    else:
        form = ProductForm(instance=product)
    context = {
        'product': product,
        'form' : form,
        'room_name': "broadcast",
    }
    return render(request,'sales/update.html', context)


@login_required
def delete(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.user == product.user:
        product.delete()
    return redirect('sales:index')


@login_required
def delete_review(request, product_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'})


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
    
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.score = request.POST.get('score')
            review.product = product
            review.save()
            return redirect('sales:detail', product_pk)
    else:
        review_form = ReviewForm()
    context = {
        'product': product,
        'review_form': review_form,
        'room_name': "broadcast",
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

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'})


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
