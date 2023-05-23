from django.shortcuts import render,redirect
from .forms import GardenForm


# Create your views here.
def create(request):
    if request.method == 'POST':
        form = GardenForm(request.POST, request.FILES)
        if form.is_valid():
            fo = form.save(commit=False)
            fo.user = request.user
            fo.save()
            return redirect('')
        else:
            print(form.errors)
    else:
        form = GardenForm()
    context = {
        'form': form,
    }
    return render(request, '', context)


def delete(request, garden_pk):
    garden = garden.objects.get(pk=garden_pk)
    if request.user == garden.user:
        garden.delete()
    return redirect(':index')


def comment(request):
    pass


def update(request):
    pass


def like_garden(request):
    pass