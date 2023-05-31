from django.shortcuts import render,redirect

from .forms import GardenForm, CommentForm
from .models import Garden, Comment
from django.contrib import messages
from django.core.paginator import Paginator
# import requests


def searchAddressToCoordinate(address):
    # 네이버 지도 API 요청 URL
    url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode'

    # 네이버 지도 API 호출에 필요한 클라이언트 ID와 클라이언트 시크릿 키
    client_id = 'tzzd5t1bsm'
    client_secret = 'WvHndRJHuYMd7vWbfrzUXdAHC7H7Ptqw7dWAhYzm'

    # API 요청 파라미터 설정
    params = {
        'query': address,
    }

    # API 호출을 위한 헤더 설정
    headers = {
        'X-NCP-APIGW-API-KEY-ID': 'tzzd5t1bsm',
        'X-NCP-APIGW-API-KEY': 'WvHndRJHuYMd7vWbfrzUXdAHC7H7Ptqw7dWAhYzm',
    }

    # API 호출 및 응답 처리
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # API 응답에서 위도와 경도 추출
    if 'status' in data and data['status'] == 'OK' and 'addresses' in data and len(data['addresses']) > 0:
        latitude = data['addresses'][0]['y']
        longitude = data['addresses'][0]['x']
        return latitude, longitude

    # 위도와 경도를 찾을 수 없는 경우 None 반환
    return None, None


# Create your views here.
def index(request):
    gardens = Garden.objects.order_by('id')
    paginator = Paginator(gardens, 4)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number) 
    
    content = {
        'page_obj': page_obj,
    }
    return render(request, 'gardens/index.html', content)



def create(request):
    if request.method == 'POST':
        form = GardenForm(request.POST, request.FILES)
        if form.is_valid():
            fo = form.save(commit=False)
            fo.user = request.user
            fo.save()
            return redirect('gardens:index')
        else:
            messages.error(request, '폼을 올바르게 입력해주세요.')  # 오류 메시지 추가
            print(form.errors)
    else:
        form = GardenForm()
    context = {
        'form': form,
    }
    return render(request, 'gardens/create.html', context)


def delete(request,garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    if request.user == garden.user:
        garden.delete()
    return redirect('gardens:index')


def comment(request, garden_pk):
    garden = Garden.objects.get(pk=garden_pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.garden = garden
            comment.user = request.user
            comment.save()
            return redirect('gardens:detail', garden_pk)
    else:
        comment_form = CommentForm()

    context = {
        'garden': garden,
        'comment_form': comment_form,
    }
    return render(request, 'gardens/detail.html', context)

def comment_delete(request, garden_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('gardens:detail', garden_pk)



def update(request, garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    if request.method == 'POST':
        form = GardenForm(request.POST, request.FILES, instance=garden)
        if form.is_valid():
            form.save()
            return redirect('gardens:detail', garden.pk)
        else:
            print(form.errors)
    else:
        form = GardenForm(instance=garden)
        return redirect('gardens:detail', garden.pk)
    
    context = {
        'garden' : garden,
        'form': form,
    }
    return render(request, 'gardens/update.html', context)


def like_garden(request, garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    if garden.like_users.filter(pk=request.user.pk).exists():
        garden.like_users.remove(request.user)
    else:
        garden.like_users.add(request.user)
    return redirect('gardens:detail', garden_pk=garden_pk)


def listing(request):
    category = request.GET.get('category') 

    if category == '전체':  
        gardens = Garden.objects.all()
    else:  
        gardens = Garden.objects.filter(category=category)

    paginator = Paginator(gardens, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'gardens': page_obj,
    }
    return render(request, 'gardens/listing.html', context)

def detail(request, garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    comments = garden.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.garden = garden
            comment.user = request.user
            comment.save()
            return redirect('gardens:detail', garden_pk=garden_pk)
    else:
        comment_form = CommentForm()

    address = garden.address  # 주소 정보 가져오기
    latitude, longitude = searchAddressToCoordinate(address)  # 주소를 이용해 위도와 경도 검색

    context = {
        'garden': garden,
        'comments': comments,
        'comment_form': comment_form,
        'latitude': latitude,
        'longitude': longitude,
    }
    return render(request, 'gardens/detail.html', context)


def show_map(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    address = garden.address
    latitude, longitude = searchAddressToCoordinate(address)
    context = {
        'latitude': latitude,
        'longitude': longitude
    }
    return render(request, 'gardens/map.html', context)
