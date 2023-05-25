from django.shortcuts import render, redirect
from .models import Plant, PlantImage
from .forms import PlantForm, PlantImageForm
from django.contrib.auth.decorators import login_required
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
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant.save()

            images = request.FILES.getlist('images')
            for image in images:
                PlantImage.objects.create(plant=plant, image=image)
                
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

    category_list = []
    if plant is not None and "[" in plant.category:
        category_word = ""
        for category in plant.category:
            if category in ["[", "'",]:
                pass
            elif category in [",", "]"]:
                category_list.append(category_word.strip())
                category_word = ""
            else:
                category_word = category_word + category
    else:
        category_list = []


    preferences_list = []
    if plant is not None and "[" in plant.preferences:
        preferences_word = ""
        for preferences in plant.preferences:
            if preferences in ["[", "'",]:
                pass
            elif preferences in [",", "]"]:
                preferences_list.append(preferences_word.strip())
                preferences_word = ""
            else:
                preferences_word = preferences_word + preferences
    else:
        preferences_list = []


    allergy_list = []
    if plant is not None and "[" in plant.allergy:
        allergy_word = ""
        for allergy in plant.allergy:
            if allergy in ["[", "'", ",", "]"]:
                continue
            else:
                allergy_word = allergy_word + allergy
        allergy_list = allergy_word.split()
    else:
        allergy_list = []

    flowering_list = []
    if plant is not None and "[" in plant.flowering:
        flowering_word = ""
        for flowering in plant.flowering:
            if flowering in ["[", "'", ",", "]"]:
                continue
            else:
                flowering_word = flowering_word + flowering
        flowering_list = flowering_word.split()
    else:
        flowering_list = []

    season_list = []
    if plant is not None and "[" in plant.season:
        season_word = ""
        for season in plant.season:
            if season in ["[", "'", ",", "]"]:
                continue
            else:
                season_word = season_word + season
        season_list = season_word.split()
    else:
        season_list = []

    watering_list = []
    if plant is not None and "[" in plant.watering:
        watering_word = ""
        for watering in plant.watering:
            if watering in ["[", "'", ",", "]"]:
                continue
            else:
                watering_word = watering_word + watering
        watering_list = watering_word.split()
    else:
        watering_list = []

    sunlight_list = []
    if plant is not None and "[" in plant.sunlight:
        sunlight_word = ""
        for sunlight in plant.sunlight:
            if sunlight in ["[", "'", ",", "]"]:
                continue
            else:
                sunlight_word = sunlight_word + sunlight
        sunlight_list = sunlight_word.split()
    else:
        sunlight_list = []

    humidity_list = []
    if plant is not None and "[" in plant.humidity:
        humidity_word = ""
        for humidity in plant.humidity:
            if humidity in ["[", "'", ",", "]"]:
                continue
            else:
                humidity_word = humidity_word + humidity
        humidity_list = humidity_word.split()
    else:
        humidity_list = []

    temperature_list = []
    if plant is not None and "[" in plant.temperature:
        temperature_word = ""
        for temperature in plant.temperature:
            if temperature in ["[", "'", ",", "]"]:
                continue
            else:
                temperature_word = temperature_word + temperature
        temperature_list = temperature_word.split()
    else:
        temperature_list = []

    birthflower_list = []
    if plant is not None and "[" in plant.birthflower:
        birthflower_word = ""
        for birthflower in plant.birthflower:
            if birthflower in ["[", "'", ",", "]"]:
                continue
            else:
                birthflower_word = birthflower_word + birthflower
        birthflower_list = birthflower_word.split()
    else:
        birthflower_list = []
    print(temperature_list)
    context = {
        'plant':plant,
        'category_list':category_list,
        'preferences_list':preferences_list,
        'allergy_list':allergy_list,
        'flowering_list':flowering_list,
        'season_list':season_list,
        'watering_list':watering_list,
        'sunlight_list':sunlight_list,
        'humidity_list':humidity_list,
        'temperature_list':temperature_list,
        'birthflower_list':birthflower_list,
    }
    return render(request, 'plants/detail.html', context)