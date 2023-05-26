from django.shortcuts import render, redirect
from .models import Plant, PlantImage
from .forms import PlantForm, PlantImageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count

# Create your views here.
def index(request):
    plants = Plant.objects.all()
    context = {
        'plants':plants,
    }
    return render(request, 'plants/index.html', context)

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
            return redirect('plants:index')
    else:
        form = PlantForm()
        imageForm = PlantImageForm()
    context = {
        'form':form,
        'imageForm':imageForm,
    }
    return render(request, 'plants/create.html', context)


def update(request, plant_pk):
    plant = Plant.objects.get(pk=plant_pk)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plants:index')
    else:
        form = PlantForm(instance=plant)
    context = {
        'form':form,
        'plant_pk':plant_pk,
        'plant':plant,
    }
    return render(request, 'plants/update.html', context)


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
    preferences_list = extract_list(plant.preferences)
    allergy_list = extract_list(plant.allergy)
    flowering_list = extract_list(plant.flowering)
    season_list = extract_list(plant.season)
    watering_list = extract_list(plant.watering)
    sunlight_list = extract_list(plant.sunlight)
    humidity_list = extract_list(plant.humidity)
    temperature_list = extract_list(plant.temperature)
    birthflower_list = extract_list(plant.birthflower)

    context = {
        'plant': plant,
        'category_list': category_list,
        'preferences_list': preferences_list,
        'allergy_list': allergy_list,
        'flowering_list': flowering_list,
        'season_list': season_list,
        'watering_list': watering_list,
        'sunlight_list': sunlight_list,
        'humidity_list': humidity_list,
        'temperature_list': temperature_list,
        'birthflower_list': birthflower_list,
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
    }
    return JsonResponse(context)


def recommendation(request):
    plant_likes = Plant.objects.annotate(num_likes = Count('likes')).order_by('-num_likes')
    context = {
        'plant_likes':plant_likes,
    }
    return render(request, 'plants/recommendation.html', context)