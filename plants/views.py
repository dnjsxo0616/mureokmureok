from django.shortcuts import render, redirect
from .models import Plant, PlantImage
from .forms import PlantForm, PlantImageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
def index(request):
    plants = Plant.objects.order_by('-id')
    paginator = Paginator(plants, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'room_name': "broadcast",
    }
    return render(request, 'plants/index.html', context)


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def create(request):
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


# @user_passes_test(lambda u: u.is_superuser)
def update(request, plant_pk):
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


# @user_passes_test(lambda u: u.is_superuser)
def delete(request, plant_pk):
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
    # preferences_list = extract_list(plant.preferences)
    # allergy_list = extract_list(plant.allergy)
    flowering_list = extract_list(plant.flowering)
    season_list = extract_list(plant.season)
    watering_list = extract_list(plant.watering)
    sunlight_list = extract_list(plant.sunlight)
    humidity_list = extract_list(plant.humidity)
    temperature_list = extract_list(plant.temperature)
    # birthflower_list = extract_list(plant.birthflower)
    allergy = plant.allergy

    context = {
        'plant': plant,
        'category_list': category_list,
        # 'preferences_list': preferences_list,
        # 'allergy_list': allergy_list,
        'flowering_list': flowering_list,
        'season_list': season_list,
        'watering_list': watering_list,
        'sunlight_list': sunlight_list,
        'humidity_list': humidity_list,
        'temperature_list': temperature_list,
        # 'birthflower_list': birthflower_list,
        'allergy': allergy,
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
    context = {
        'filtered_plants': filtered_plants,
        'room_name': "broadcast"
    }
    return render(request, 'plants/filter.html', context)
