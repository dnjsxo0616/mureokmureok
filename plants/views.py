from django.shortcuts import render, redirect
from .models import Plant
from .forms import PlantForm
# Create your views here.
def create_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant.save()
            return redirect('')
        else:
            form = PlantForm()
        return render(request, '')
    

def update_plant(request, plant_pk):
    plant = Plant.objects.get(pk = plant_pk)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = PlantForm(instance=plant)
    return render(request, '')


def delete_plant(request, plant_pk):
    plant = Plant.objects.get(pk=plant_pk)
    if request.user == plant.user:
        plant.delete()
    return redirect('')