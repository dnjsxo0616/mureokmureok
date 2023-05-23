from django.shortcuts import render, redirect
from .models import Supply

# Create your views here.

def supply_create(request):
    if request.method == 'POST':
        # 상품 생성 로직 구현
        pass
    else:
        # GET 요청 시 상품 생성 폼 보여주기
        return render(request, 'supply_create.html')


def supply_detail(request, supplies_pk):
    pass


def supply_delete(request, supply_pk):
    supply = supply.objects.get(pk=supply_pk)
    if request.user == supply.user:
        supply.delete()
    return redirect(':index')

def supply_update(request):
    pass


def filter_products(request):
    selected_tags = request.GET.getlist('tags')
    products = Supply.objects.filter(tags__in=selected_tags)
    context = {'products': products, 'selected_tags': selected_tags}
    return render(request, 'filter_products.html', context)
