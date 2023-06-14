from django.shortcuts import render, redirect
from .models import Plant, PlantImage
from .forms import PlantForm, PlantImageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from sales.models import Product


# Create your views here.
def index(request):
    plants = Plant.objects.order_by('-id')
    paginator = Paginator(plants, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    unique_tags = []
    all_tags = []
    for plant in page_obj:
        for tag in plant.tags.all():
            if tag.name not in all_tags:
                all_tags.append(tag.name)
                unique_tags.append(tag.name)

    context = {
        'page_obj': page_obj,
        'unique_tags': unique_tags[:10],
        'room_name': "broadcast",
    }
    return render(request, 'plants/index.html', context)



@login_required(login_url='admin:login')
def create(request):

    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        tags = request.POST.get('tags').split(',')
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant.save()

            images = request.FILES.getlist('images')
            for image in images:
                PlantImage.objects.create(plant=plant, image=image)
            
            for tag in tags:
                plant.tags.add(tag.strip())
            return redirect('plants:detail', plant.pk)
    else:
        form = PlantForm()
        imageForm = PlantImageForm()
    context = {
        'form':form,
        'imageForm':imageForm,
        'room_name': "broadcast"
    }
    return render(request, 'plants/create.html', context)



def update(request, plant_pk):
    
    if not request.user.is_superuser:
        return redirect('home')
    
    plant = Plant.objects.get(pk=plant_pk)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            plant.tags.clear()
            tags = request.POST.get('tags').split(',')
            for tag in tags:
                plant.tags.add(tag.strip())
            return redirect('plants:detail', plant_pk)
    else:
        form = PlantForm(instance=plant)
    context = {
        'form':form,
        'plant_pk':plant_pk,
        'plant':plant,
        'room_name': "broadcast"
    }
    return render(request, 'plants/update.html', context)



def delete(request, plant_pk):
    
    if not request.user.is_superuser:
        return redirect('home')
    
    plant = Plant.objects.get(pk=plant_pk)
    if request.user == plant.user:
        plant.delete()
    return redirect('plants:index')


def detail(request, plant_pk):
    plant = Plant.objects.get(pk=plant_pk)

    def extract_list(field):
        if plant is not None and "[" in field:
            word = ""
            for item in field:
                if item in ["[", "'", ",", "]"]:
                    continue
                else:
                    word += item
            return word.split()
        else:
            return []
        
    category_list = extract_list(plant.category)
    watering_list = extract_list(plant.watering)
    sunlight_list = extract_list(plant.sunlight)
    humidity_list = extract_list(plant.humidity)
    temperature_list = extract_list(plant.temperature)
    allergy = plant.allergy


    # filtered_products = []
    # products = Product.objects.all()
    
    # print(products)
    # product_title = []
    # for product in products:
    #     tags = product.tags.all()
    #     for tag in tags:
    #         if '따뜻한' in tag.name:
    #             product_title.append(product.title)
    # print(product_title)

        # 위에서는 나오는데 아래서 안나오네요
    # product_titles = []
    # if watering_list == '주1~2회':
    #     products = Product.objects.all()
    #     products = Product.objects.filter(tags__name='따뜻한')
    #     for product in products:
    #         print(product.title)


    # watering_plants = Plant.objects.filter(watering='주1~2회')
    # watering_products = Product.objects.filter(tags_name='따뜻한', plant__in=watering_plants)

    # product_titles = []
    # filtered_products = Product.objects.filter(tags__name__in='따뜻한')
  
    # if plant.watering == '주1~2회':
    #     for product in products:
       
    #         tags = product.tags.all()
    #         for tag in tags:
    #             if '따뜻한' in tag.name: # 이건 product
    #                 product_titles.append(product.title)
    #         # elif watering_list == '월1~2회':
    #         #     if '월1~2회 태그' in product.tags:
    #         #         filtered_products.append(product)
    #         # elif watering_list == '월1회이하':
    #         #     if '월1회이하 태그' in product.tags:
    #         #         filtered_products.append(product)
    #         # elif watering_list == '주2~3회':
    #         #     if '주2~3회 태그' in product.tags:
    #         #         filtered_products.append(product)

    products = Product.objects.all()
   

    context = {
        'plant': plant,
        'category_list': category_list,

        'watering_list': watering_list,
        'sunlight_list': sunlight_list,
        'humidity_list': humidity_list,
        'temperature_list': temperature_list,
        'allergy': allergy,
        'products':products,
    }
    return render(request, 'plants/detail.html', context)


@login_required
def likes(request, plant_pk):
    plant = Plant.objects.get(pk=plant_pk)

    if request.user in plant.like_users.all():
        plant.like_users.remove(request.user)
        is_liked=False
    else:
        plant.like_users.add(request.user)
        is_liked=True

    context = {
        'is_liked' : is_liked,
        'like_count': plant.like_users.count(),
    }
    return JsonResponse(context)


def recommendation(request):
    recommended_plants = Plant.objects.annotate(like_count=Count('like_users')).order_by('-like_count')  # 좋아요 순으로 정렬
    context = {
        'recommended_plants': recommended_plants,
        'room_name': "broadcast"
    }
    return render(request, 'plants/recommendation.html', context)


def search(request):
    query = request.GET.get('searched', '')
    plants = Plant.objects.filter(title__contains=query)

    context = {
        'plants':plants,
        'query':query,
        'room_name': "broadcast"
    }
    return render(request, 'plants/search.html', context)


def filter_plants(request, tag):
    filtered_plants = Plant.objects.filter(tags__name__in=[tag])
    unique_tags = Plant.objects.values_list('tags__name', flat=True).distinct()

    context = {
        'filtered_plants': filtered_plants,
        'unique_tags': unique_tags,
        'room_name': "broadcast"
    }

    return render(request, 'plants/filter.html', context)


def category_plants(request):
    category = request.GET.getlist('category')

    if '전체' in category:
        filtered_plants = Plant.objects.all()
    elif '실내식물' in category:
        filtered_plants = Plant.objects.filter(category__contains='실내식물')
    elif '실외식물' in category:
        filtered_plants = Plant.objects.filter(category__contains='실외식물')
    else:
        filtered_plants = Plant.objects.none()

    context = {
        'filtered_plants': filtered_plants,
        'category': category,
    }
    return render(request, 'plants/category.html', context)





