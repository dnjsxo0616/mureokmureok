from django.shortcuts import render, redirect
from .models import Management, CalenderEntry
from .forms import ManagementForm, CalenderEntryForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from django.views import View
from datetime import datetime, date, timedelta
from plants.models import Plant
from accounts.models import User, User_title, User_profile
import calendar
import datetime
import math
import re

# Create your views here.







def detail(request, management_pk):
    management = Management.objects.get(pk=management_pk)
    calenderentrys = management.calenderentry_set.all()
    entries = CalenderEntry.objects.filter(management=management)
    today = date.today()
    year = today.year
    month = today.month
    _, num_days = calendar.monthrange(year, month)
    first_day_of_month = date(year, month, 1)
    first_day_of_week = first_day_of_month.weekday()
    first_day_of_week = (first_day_of_week + 1) % 7

    calendar_days = []
    week_data = []
    week_data.extend([None] * first_day_of_week)

    for day in range(1, num_days + 1):
        week_data.append(date(year, month, day))
        if len(week_data) == 7:
            calendar_days.append(week_data)
            week_data = []

    # 마지막 주의 나머지 빈 날짜 칸 생성
    if week_data:
        week_data.extend([None] * (7 - len(week_data)))
        calendar_days.append(week_data)

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



    # score 계산
    score = 0
    start_date = date.today() - timedelta(days=6)
    end_date = date.today()

    # watering_numbers 추출
    watering_data = management.plant.watering
    numbers = re.findall(r'\d+', watering_data)
    watering_numbers = [int(num) for num in numbers]

    watering_yes_entries_count = CalenderEntry.objects.filter(
        management=management,
        entrydate__range=[start_date, end_date],
        watering="yes"
    ).count()


    if watering_numbers[0] <= watering_yes_entries_count <= watering_numbers[1]:
        score += 20
    elif watering_yes_entries_count == watering_numbers[0] + 2:
        score += 15
    elif watering_yes_entries_count == watering_numbers[0] + 3:
        score += 10
    elif watering_yes_entries_count < watering_numbers[0]:
        difference = watering_numbers[0] - watering_yes_entries_count
        if difference == 1:
            score += 15
        elif difference == 2:
            score += 10
        else:
            score += 5
    else:
        score += 5

    sunlight_level = management.plant.sunlight
    

    sunlight_yes_entries_count = CalenderEntry.objects.filter(
        management=management,
        entrydate__range=[start_date, end_date],
        sunlight="yes"
    ).count()

    if '양지' in sunlight_level:
        if sunlight_yes_entries_count >= 4:
            score += 20
        elif sunlight_yes_entries_count == 3:
            score += 15
        elif sunlight_yes_entries_count == 2:
            score += 10
        else:
            score += 5

    elif '반양지' in sunlight_level:
        if sunlight_yes_entries_count == 5:
            score += 10
        elif sunlight_yes_entries_count == 4:
            score += 15
        elif sunlight_yes_entries_count == 3:
            score += 20
        elif sunlight_yes_entries_count == 2:
            score += 15
        elif sunlight_yes_entries_count == 1:
            score += 10
        else:
            score += 5

    elif '반음지' in sunlight_level:
        if sunlight_yes_entries_count == 3:
            score += 15
        elif sunlight_yes_entries_count == 4:
            score += 10
        elif sunlight_yes_entries_count == 2:
            score += 20
        elif sunlight_yes_entries_count == 1:
            score += 15
        elif sunlight_yes_entries_count == 0:
            score += 10
        else:
            score += 5

    elif '음지' in sunlight_level:
        if sunlight_yes_entries_count == 1:
            score += 15
        elif sunlight_yes_entries_count == 2:
            score += 10
        elif sunlight_yes_entries_count == 0:
            score += 20
        else:
            score += 5


    humidity_level = management.plant.humidity
    
    humidity_another_entries_count = CalenderEntry.objects.filter(
        management=management,
        entrydate__range=[start_date, end_date],
    ).exclude(humidity=humidity_level).count()

    
    if humidity_another_entries_count == 0:
        score += 20
    elif humidity_another_entries_count == 1:
        score += 15
    elif humidity_another_entries_count == 2:
        score += 10

    elif humidity_another_entries_count >= 3:
        score += 5
    else:
        score += 5

    temperature_level = management.plant.temperature
    
    temperature_another_entries_count = CalenderEntry.objects.filter(
        management=management,
        entrydate__range=[start_date, end_date],
    ).exclude(temperature=temperature_level).count()

    
    if temperature_another_entries_count == 0:
        score += 20
    elif temperature_another_entries_count == 1:
        score += 15
    elif temperature_another_entries_count == 2:
        score += 10
    elif temperature_another_entries_count >= 3:
        score += 5
    else:
        score += 5


    management.score = score
    management.save()
    

    context ={
        'management' : management,
        'calenderentrys' : calenderentrys,
        'calenderentry_form': calenderentry_form,
        'entries': entries,
        'calendarData': calendar_days,
        'room_name': "broadcast"
    }
    return render(request,'managements/detail.html', context)




def index(request):
    managements = Management.objects.all()
    context = {
        'managements': managements,
        'room_name': "broadcast"
    }
    return render(request, 'managements/index.html', context)



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
