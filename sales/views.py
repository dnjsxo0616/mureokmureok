# from django.shortcuts import render, redirect
# from .models import Product, Purchase, Cart
# from .forms import ProductForm, PurchaseForm
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.core.paginator import Paginator
# from accounts.models import User, User_title, User_profile
# from django.db.models import Count, Q
# from django.http import JsonResponse


# def index(request):
#     products = Product.objects.all()
#     context = {
#         'products': products, 
#     }
#     return render(request, 'sales/index.html', context)



# @login_required
# def create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.user = request.user
#             product.save()
#             return redirect('sales:detail', product.pk)
#     else:
#         form = ProductForm()
#     context = {
#         'form' : form,
#     }
#     return render(request, 'sales/create.html', context)



# def detail(request, product_pk):
#     product = Product.objects.get(pk=product_pk)
#     products = Product.objects.all().order_by('like')

#     context ={
#         'product' : product,
#         'products': products,
#     }
#     return render(request,'sales/detail.html', context)



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