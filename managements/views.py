from django.shortcuts import render, redirect
from .models import Management, CalenderEntry
from .forms import ManagementForm, CalenderEntryForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from django.views import View
from datetime import datetime
from plants.models import Plant
from accounts.models import User, User_title, User_profile

# Create your views here.

def index(request):
    managements = Management.objects.all()
    context = {
        'managements': managements,
        'room_name': "broadcast"
    }
    return render(request, 'managements/index.html', context)



def detail(request, management_pk):
    management = Management.objects.get(pk=management_pk)
    calenderentrys = management.calenderentry_set.all()

    if request.method == 'POST':
        calenderentry_form = CalenderEntryForm(request.POST, request.FILES)
        if calenderentry_form.is_valid():
            calenderentry = calenderentry_form.save(commit=False)
            calenderentry.management = management
            calenderentry.user = request.user
            calenderentry.save()
            return redirect('managements:detail', management_pk=management_pk)
    else:
        calenderentry_form = CalenderEntryForm()

    context ={
        'management' : management,
        'calenderentrys' : calenderentrys,
        'calenderentry_form': calenderentry_form,
        'room_name': "broadcast"
    }
    return render(request,'managements/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ManagementForm(request.POST, request.FILES)
        if form.is_valid():
            management = form.save(commit=False)

            management.user = request.user
            management.save()

            return redirect('managements:detail', management.pk)
    else:
        form = ManagementForm()
    context = {
        'form' : form,
        'room_name': "broadcast"
    }
    return render(request, 'managements/create.html', context)



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



def calenderentry_create(request, management_pk):
    management = Management.objects.get(pk=management_pk)

    if request.method == 'POST':
        calenderentry_form = CalenderEntryForm(request.POST, request.FILES)
        if calenderentry_form.is_valid():
            calenderentry = calenderentry_form.save(commit=False)
            calenderentry.management = management
            calenderentry.user = request.user
            calenderentry.save()
            return redirect('managements:detail', management_pk)
    else:
        calenderentry_form = CalenderEntryForm()

    context = {
        'management': management,
        'calenderentry_form': calenderentry_form,
        'room_name': "broadcast"
    }
    return render(request, 'managements/detail.html', context)




@login_required
def calenderentry_update(request, management_pk, calenderentry_pk):
    calenderentry = calenderentry.objects.get(pk=calenderentry_pk)
    if request.user == calenderentry.user:
        if request.method == 'POST':
            calenderentry_form = CalenderEntryForm(request.POST, instance=calenderentry)
            if calenderentry_form.is_valid():
                calenderentry_form.save()
                return redirect('managements:detail', management_pk)
                # return JsonResponse({'status': 'success'})
        else:
            calenderentry_form = CalenderEntryForm(instance=calenderentry)
        context = {
            'calenderentry_form': calenderentry_form,
            'calenderentry': calenderentry,
        }
        return render(request, 'managements/detail.html', context)



@login_required
def calenderentry_delete(request, management_pk, calenderentry_pk):
    calenderentry = CalenderEntry.objects.get(pk=calenderentry_pk)
    if request.user == calenderentry.user:
        calenderentry.delete()

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'})
