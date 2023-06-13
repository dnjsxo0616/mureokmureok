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
# csrf 권한 해제
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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
        tags = request.POST.get('tags').split(',')
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

            for tag in tags:
                product.tags.add(tag.strip())
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


# def sort(request, *args, **kwargs):
#     sort_type = request.GET.get('sort_type')
#     queryset = super().get_queryset()

#     if sort_type == 'popularity':
#         queryset = queryset.order_by('-views')
#     elif sort_type == 'latest':
#         queryset = queryset.order_by('-created_at')
#     elif sort_type == 'price_low':
#         queryset = queryset.order_by('price')
#     elif sort_type == 'price_high':
#         queryset = queryset.order_by('-price')

#     data = serializers.serialize('json', queryset)

#     paginator = Paginator(data, 16)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj,
#         'room_name': "broadcast",
#     }
#     return JsonResponse(context, safe=False)


@login_required
def update(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            product.tags.clear()
            tags = request.POST.get('tags').split(',')
            for tag in tags:
                product.tags.add(tag.strip())
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
        total_price = (product_info['quantity']) * product.price
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


def create_order(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0
    cart_total_quantity = 0
    cart_product = ''
    for product_pk, product_info in cart.items():
  
        product = Product.objects.get(pk=product_pk)
        total_price = (product_info['quantity']) * product.price
        cart_total += total_price
        cart_total_quantity += product_info['quantity']
        cart_product += product.title + ' '

        cart_items.append({
            'product': product,
            'quantity': product_info['quantity'],
            'total_price': total_price,
            'cart_product':cart_product,
        })
        print(cart_items)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid(): 
            order = form.save(commit=False)
            order.user = request.user
            order.save()
                # 주문 정보 처리 (예: 결제 등)
                # ...
            
            # 주문 완료 후 장바구니 비우기
            # ...
            
            return redirect('sales:order_payment', order.pk)
    else:
        form = OrderForm()
    context ={
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_total_quantity':cart_total_quantity,
        'cart_product': cart_product,
    }

    return render(request, 'sales/create_order.html', context)

def create_ordernow(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('sales:order_payment', order.pk)
    else:
        form = OrderForm()
    context = {
        'form':form,
        'product':product,

    }
    return render(request, 'sales/create_ordernow.html', context)

# 1 바로 넘어가는 것
# def order_complete(request):
#     # 주문 객체 검색 코드 (예시)
#     order = Order.objects.last()  # 가장 최근에 생성된 주문 객체를 가져옴

#     if order is not None:
#         order_number = order.order_number
#         return redirect('sales:order_detail', order_number=order_number)
#     else:
#         return render(request, 'sales/order_complete.html')

def order_complete(request):
    # 주문 객체 검색 코드 (예시)
    order = Order.objects.last()  # 가장 최근에 생성된 주문 객체를 가져옴

    context = {
        'order':order,
    }

    return render(request, 'sales/order_complete.html', context)



def order_payment(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    context = {
        'order': order
    }
    return render(request, 'sales/order_payment.html', context)

def delete_order(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    if request.method == 'POST':
        # 주문 삭제
        order.delete()
        return redirect('sales:index')

    context = {
        'order': order
    }

    return render(request, 'sales/order_payment.h', context)


# def order_complete(request, order_pk):
#     order = Order.objects.get(pk=order_pk)
#     context = {
#         'order': order,
#     }
#     return render(request, 'sales/order_complete.html', context)

def order_detail(request, order_number):
    order = Order.objects.get(order_number=order_number)
    context = {
        'order':order,
    }
    return render(request, 'sales/order_detail.html', context)

@login_required 
def order_list(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {
        'orders':orders,
    }
    return render(request, 'sales/order_list.html', context)


def order_cancel(request):
    return render(request, 'sales/order_cancel.html')

@method_decorator(csrf_exempt, name='dispatch')
def juso_popup(request):
    inputYn = request.GET.get('inputYn')
    roadFullAddr = request.GET.get('roadFullAddr')
    context = {
        'inputYn': inputYn,
        'roadFullAddr':roadFullAddr,
    }
    return render(request, 'sales/jusoPopup.html', context)


def jusopopuptest(request):
    return render(request, 'sales/jusopopup.html')

def sampletest(request):
    return render(request, 'sales/sampletest.html')
