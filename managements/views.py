from django.shortcuts import render, redirect
from .models import Management, CalenderEntry
from .forms import ManagementForm, CalenderEntryForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from django.views import View
from datetime import datetime, date, timedelta
from plants.models import Plant
from django.utils import timezone
from accounts.models import User, User_title, User_profile
import calendar
import datetime
import math
import re
from django.contrib.auth import logout
from django.shortcuts import redirect

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
    watering_score = 0
    sunlight_score = 0
    humidity_score = 0
    temperature_score = 0

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

    watering_score_reason = ''

    if watering_numbers[0] <= watering_yes_entries_count <= watering_numbers[1]:
        score += 20
        watering_score = 20
        watering_score_reason = '물을 잘 주시고 계시네요!'
    elif watering_yes_entries_count == watering_numbers[0] + 2:
        score += 15
        watering_score = 15
        watering_score_reason = '물주기를 조금 줄여보세요!'
    elif watering_yes_entries_count == watering_numbers[0] + 3:
        score += 10
        watering_score = 15
        watering_score_reason = '물을 너무 많이 주고 계시네요!'
    elif watering_yes_entries_count == watering_numbers[0] + 4:
        score += 5
        watering_score = 5
        watering_score_reason = '꾸르륵 꾸르륵...(물에 잠기는 소리)'
    elif watering_yes_entries_count < watering_numbers[0]:
        difference = watering_numbers[0] - watering_yes_entries_count
        if difference == 1:
            score += 15
            watering_score = 15
            watering_score_reason = '물을 조금 덜 주고 계시네요!'
        elif difference == 2:
            score += 10
            watering_score = 10
            watering_score_reason = '친구가 목이 마르다는데요..'
        else:
            score += 5
            watering_score = 5
            watering_score_reason = '곧 말라버릴지도...'
    else:
        score += 5
        watering_score = 5
        watering_score_reason = '일지에 기록해보세요!'

    sunlight_level = management.plant.sunlight
    

    sunlight_yes_entries_count = CalenderEntry.objects.filter(
        management=management,
        entrydate__range=[start_date, end_date],
        sunlight="yes"
    ).count()

    sunlight_score_reason = ''

    if '양지' in sunlight_level:
        if sunlight_yes_entries_count >= 4:
            score += 20
            sunlight_score = 20
            sunlight_score_reason = '햇빛 양이 충분해요!'
        elif sunlight_yes_entries_count == 3:
            score += 15
            sunlight_score = 15
            sunlight_score_reason = '햇빛 양이 살짝 부족해요!'
        elif sunlight_yes_entries_count == 2:
            score += 10
            sunlight_score = 10
            sunlight_score_reason = '햇빛 양이 많이 부족해요!'
        else:
            score += 5
            sunlight_score = 5
            sunlight_score_reason = '친구가 빛이 보고싶다는데요...'

    elif '반양지' in sunlight_level:
        if sunlight_yes_entries_count == 5:
            score += 10
            sunlight_score = 10
            sunlight_score_reason = '햇빛 양이 너무 많아요!'
        elif sunlight_yes_entries_count == 4:
            score += 15
            sunlight_score = 15
            sunlight_score_reason = '햇빛 양이 조금 많아요!'
        elif sunlight_yes_entries_count == 3:
            score += 20
            sunlight_score = 20
            sunlight_score_reason = '햇빛 양이 충분해요!'
        elif sunlight_yes_entries_count == 2:
            score += 15
            sunlight_score = 15
            sunlight_score_reason = '햇빛 양이 살짝 부족해요!'
        elif sunlight_yes_entries_count == 1:
            score += 10
            sunlight_score = 10
            sunlight_score_reason = '햇빛 양이 많이 부족해요!'
        else:
            score += 5
            sunlight_score = 5
            sunlight_score_reason = '친구가 빛이 보고싶다는데요...'

    elif '반음지' in sunlight_level:
        if sunlight_yes_entries_count == 3:
            score += 15
            sunlight_score = 15
            sunlight_score_reason = '햇빛 양이 조금 많아요!'
        elif sunlight_yes_entries_count == 4:
            score += 10
            sunlight_score = 10
            sunlight_score_reason = '햇빛 양이 너무 많아요!'
        elif sunlight_yes_entries_count == 2:
            score += 20
            sunlight_score = 20
            sunlight_score_reason = '햇빛 양이 충분해요!'
        elif sunlight_yes_entries_count == 1:
            score += 15
            sunlight_score = 15
            sunlight_score_reason = '햇빛 양이 살짝 부족해요!'
        elif sunlight_yes_entries_count == 0:
            score += 10
            sunlight_score = 10
            sunlight_score_reason = '햇빛 양이 살짝 부족해요!'
        else:
            score += 5
            sunlight_score = 5
            sunlight_score_reason = '반음지라도 햇빛을 한번쯤은...'

    elif '음지' in sunlight_level:
        if sunlight_yes_entries_count == 1:
            score += 15
            sunlight_score = 15
            sunlight_score_reason = '햇빛 양이 조금 많아요!'
        elif sunlight_yes_entries_count == 2:
            score += 10
            sunlight_score = 10
            sunlight_score_reason = '햇빛 양이 너무 많아요!'
        elif sunlight_yes_entries_count == 0:
            score += 20
            sunlight_score = 20
            sunlight_score_reason = '햇빛 양이 충분해요!'
        else:
            score += 5
            sunlight_score = 5
            sunlight_score_reason = '음지 식물은 빛을 싫어해요..'


    humidity_level = management.plant.humidity
    
    humidity_another_entries_count = CalenderEntry.objects.filter(
        management=management,
        entrydate__range=[start_date, end_date],
    ).exclude(humidity=humidity_level).count()

    humidity_score_reason = ''
    if humidity_another_entries_count == 0:
        score += 20
        humidity_score = 20
        humidity_score_reason = '습도가 잘 맞아요!'
    elif humidity_another_entries_count == 1:
        score += 15
        humidity_score = 15
        humidity_score_reason = '최적 습도를 유지해주세요!'
    elif humidity_another_entries_count == 2:
        score += 10
        humidity_score = 10
        humidity_score_reason = '최적 습도를 많이 벗어났어요!'

    elif humidity_another_entries_count >= 3:
        score += 5
        humidity_score = 5
        humidity_score_reason = '식물의 위치를 습도가 맞는 곳으로 바꿔야 할 것 같아요!'
    else:
        score += 5
        humidity_score = 5
        humidity_score_reason = '최적 습도를 맞춰주세요!'

    temperature_level = management.plant.temperature
    
    temperature_another_entries_count = CalenderEntry.objects.filter(
        management=management,
        entrydate__range=[start_date, end_date],
    ).exclude(temperature=temperature_level).count()

    temperature_score_reason = ''
    if temperature_another_entries_count == 0:
        score += 20
        temperature_score = 20
        temperature_score_reason = '최적 온도가 잘 맞춰지고 있어요'
    elif temperature_another_entries_count == 1:
        score += 15
        temperature_score = 15
        temperature_score_reason = '최적 온도를 유지해주세요!'
    elif temperature_another_entries_count == 2:
        score += 10
        temperature_score = 10
        temperature_score_reason = '식물 위치를 온도에 맞게 바꿔보는 것은 어떠세요?'
    elif temperature_another_entries_count >= 3:
        score += 5
        temperature_score = 5
        temperature_score_reason = '최적 온도를 확인하세요!'
    else:
        score += 5
        temperature_score = 5
        temperature_score_reason = '최적 온도를 확인하세요!'

    things_yes_entries_count = CalenderEntry.objects.filter(
        management=management,
        entrydate__range=[start_date, end_date],
        things="yes"
    ).count()

    things_score_reason = ''
    if things_yes_entries_count == 1:
        score += 20
        things_score = 20
        things_score_reason = '소모품을 식물 기호에 맞게 주셔야합니다!'
    elif things_yes_entries_count == 0:
        score += 10
        things_score = 10
        things_score_reason = '소모품은 선택입니다!'
    else:
        score += 0
        things_score = 0
        things_score_reason = '너무 많이 주신 것 같아요!'


    # significant_yes_entries_count = CalenderEntry.objects.filter(
    #     management=management,
    #     entrydate__range=[start_date, end_date],
    #     significant="노란"
    # ).count()

    # significant_score_reason = ''
    # if significant_yes_entries_count == 1:
    #     score += 10
    #     significant_score_reason = '소모품을 식물 기호에 맞게 주셔야합니다!'
    # elif significant_yes_entries_count == 0:
    #     score += 5
    #     significant_score_reason = '소모품은 선택입니다!'
    # else:
    #     score += 0
    #     significant_score_reason = '너무 많이 주신 것 같아요!'


    management.score = score
    management.save()
    
    management_start_date = management.managementdate
    management_current_date = date.today()
    management_time_passed = (management_current_date - management_start_date).days

    context ={
        'management' : management,
        'calenderentrys' : calenderentrys,
        'calenderentry_form': calenderentry_form,
        'entries': entries,
        'calendarData': calendar_days,
        'watering_score': watering_score,
        'sunlight_score': sunlight_score,
        'humidity_score': humidity_score,
        'temperature_score': temperature_score,
        'things_score': things_score,
        'watering_score_reason': watering_score_reason,
        'sunlight_score_reason': sunlight_score_reason,
        'humidity_score_reason': humidity_score_reason,
        'temperature_score_reason': temperature_score_reason,
        'things_score_reason': things_score_reason,
        'management_time_passed': management_time_passed,
        'room_name': "broadcast"
    }
    return render(request,'managements/detail.html', context)



def index(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    managements = Management.objects.filter(user_id=request.user.id)
    good_plants = 0
    nice_plants = 0
    bad_plants = 0
    sum_score = 0
    average_score = 0


    for management in managements:
        sum_score += management.score
        if management.score >= 80:
            good_plants += 1
        elif management.score < 80 and management.score >= 40:
            nice_plants += 1
        elif management.score < 40:
            bad_plants += 1

    average_score = sum_score // (managements.count())

    for management in managements:
        management_start_date = management.managementdate
        if management_start_date is not None:
            management_current_date = date.today()
            management_time_passed = (management_current_date - management_start_date).days
            management.management_time_passed = management_time_passed

    context = {
        'managements': managements,
        'good_plants': good_plants,
        'nice_plants': nice_plants,
        'bad_plants': bad_plants,
        'average_score': average_score,
        'room_name': "broadcast",
    }
    
    return render(request, 'managements/index.html', context)



@login_required
def create(request):
    plants = Plant.objects.all()
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
        'plants': plants,
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
            entry_date = calenderentry_form.cleaned_data['entrydate']  
            existing_entries = CalenderEntry.objects.filter(entrydate=entry_date, user=request.user)
            if existing_entries.exists():
                return redirect('managements:detail', management_pk)
            else:
                calenderentry = calenderentry_form.save(commit=False)
                calenderentry.management = management
                calenderentry.user = request.user
                calenderentry.save()
                return redirect('managements:detail', management_pk)
        else:
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
    calenderentry = CalenderEntry.objects.get(pk=calenderentry_pk)
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



# @login_required
# def calenderentry_delete(request, management_pk, calenderentry_pk):
#     calenderentry = CalenderEntry.objects.get(pk=calenderentry_pk)
#     if request.user == calenderentry.user:
#         calenderentry.delete()

#         return JsonResponse({'status': 'ok'})
#     else:
#         return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'})

@login_required
def calenderentry_delete(request, management_pk, calenderentry_pk):
    calenderentry = CalenderEntry.objects.get(pk=calenderentry_pk)

    if request.user == calenderentry.user:
        calenderentry.delete()
    return redirect('managements:detail', management_pk)