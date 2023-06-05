from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.urls import reverse
from .models import User_profile, User_title

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            prev_url = request.session.get('prev_url')
            # 이전 페이지의 URL 정보가 있으면 해당 URL로 리다이렉트합니다.
            if prev_url:
                # 이전 페이지의 URL 정보를 삭제합니다.
                del request.session['prev_url']
                return redirect(prev_url)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    request.session['prev_url'] = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
        'room_name': "broadcast"
    }
    return render(request, 'accounts/login.html', context)



@login_required
def logout(request):
    auth_logout(request)
    request.session['prev_url'] = request.META.get('HTTP_REFERER')

    # 로그아웃 후 이전 페이지의 URL 정보가 있으면 해당 페이지로 리다이렉트합니다.
    prev_url = request.session.get('prev_url')
    if prev_url:
        # 이전 페이지의 URL 정보를 삭제합니다.
        del request.session['prev_url']
        return redirect(prev_url)
        
    return redirect('home')



def signup(request):
    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # User 객체 저장
            user_profile = User_profile.objects.create(user=user)
            user_profile.points = 0

            min_points = user_profile.points
            max_points = user_profile.points
            user_title = User_title.objects.filter(min_points__lte=min_points, max_points__gte=max_points).first()
            user_profile.title = user_title


            user_profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            prev_url = request.session.get('prev_url')
            if prev_url:
                del request.session['prev_url']
                return redirect(prev_url)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    request.session['prev_url'] = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
        'room_name': "broadcast"
    }
    return render(request, 'accounts/signup.html', context)



@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('home')



@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
        'room_name': "broadcast"
    }
    return render(request, 'accounts/update.html', context)



@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile', request.user)
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
        'room_name': "broadcast"
    }
    return render(request, 'accounts/change_password.html', context)



def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    # plants = Plant.objects.filter(user=person).order_by('-pk')
    # gardens = Garden.objects.filter(user=person).order_by('-pk')
    # communities = Community.objects.filter(user=person).order_by('-pk')
    # supplies = Supply.objects.filter(user=person).order_by('-pk')

    context = {
        'person': person,
        'room_name': "broadcast"
    }
    return render(request, 'accounts/profile.html', context)



@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user

    if you != me:
        if me in you.followers.all():
            you.followers.remove(me)
            is_followed = False
        else:
            you.followers.add(me)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': you.followings.count(),
            'followers_count': you.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', you.username)


@login_required
def user_profile(request):
    user_profile = User_profile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'user_profile': user_profile})