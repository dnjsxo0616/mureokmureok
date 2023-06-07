from django.shortcuts import render
from .models import Management
from .forms import ManagementForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def index(request):
    managements = Management.objects.all()
    context = {
        'managements': managements,
        'room_name': "broadcast"
    }
    return render(request, 'managements/index.html', context)



def detail(request, management_pk):
    management = Management.objects.get(pk = management_pk)


    context ={
        'management' : management,
        'room_name': "broadcast"
    }
    return render(request,'managements/detail.html', context)



def update(request, management_pk):
    management = Management.objects.get(pk=management_pk)
    if request.method == 'POST':
        form = ManagementForm(request.POST, request.FILES, instance=management)
        if form.is_valid():
            form.save()
            return redirect('managements:detail', management_pk)
    else:
        form = ManagementForm(instance=management)
    context = {
        'form':form,
        'management_pk': management_pk,
        'management': management,
        'room_name': "broadcast"
    }
    return render(request, 'managements/update.html', context)



def delete(request, management_pk):
    management = Management.objects.get(pk=management_pk)
    if request.user == management.user:
        management.delete()
    return redirect('managements:index')