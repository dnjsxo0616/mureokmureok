from django.shortcuts import render,redirect
from .forms import GardenForm, CommentForm
from .models import Garden, Comment
from django.contrib import messages
from django.core.paginator import Paginator
import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def index(request):
    gardens = Garden.objects.order_by('-created_at')
    paginator = Paginator(gardens, 8)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number) 
    
    content = {
        'page_obj': page_obj,
        'room_name': "broadcast"
    }
    return render(request, 'gardens/index.html', content)


def create(request):
    if request.method == 'POST':
        form = GardenForm(request.POST, request.FILES)
        if form.is_valid():
            garden = form.save(commit=False)
            garden.user = request.user
            garden.save()
            return redirect('gardens:detail', garden.pk)
        else:
            messages.error(request, '폼을 올바르게 입력해주세요.')  # 오류 메시지 추가
            print(form.errors)
    else:
        form = GardenForm()
    context = {
        'form': form,
        'room_name': "broadcast"
    }
    return render(request, 'gardens/create.html', context)


@login_required
def delete(request,garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    if request.user == garden.user:
        garden.delete()
    return redirect('gardens:index')


@login_required
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


@login_required
def comment_update(request, garden_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                return redirect('gardens:detail', garden_pk)
                # return JsonResponse({'status': 'success'})
        else:
            comment_form = CommentForm(instance=comment)
        context = {
            'comment_form': comment_form,
            'comment': comment,
        }
        return render(request, 'gardens/detail.html', context)


@login_required
def comment_delete(request, garden_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'})


@login_required
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
    context = {
        'garden' : garden,
        'form': form,
        'room_name': "broadcast"
    }
    return render(request, 'gardens/update.html', context)


@login_required
def like_garden(request, garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    if garden.like_users.filter(pk=request.user.pk).exists():
        garden.like_users.remove(request.user)
        is_liked = False
    else:
        garden.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'like_count': garden.like_users.count(),
    }
    return JsonResponse(context)


def listing(request):
    category = request.GET.get('category')

    if category == '전체':  
        gardens = Garden.objects.all().order_by('-created_at')
    else:  
        gardens = Garden.objects.filter(category=category).order_by('-created_at')

    paginator = Paginator(gardens, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'room_name': "broadcast"
    }
    return render(request, 'gardens/listing.html', context)


def detail(request, garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    comments = garden.comments.all()

    session_key = 'garden_{}_hits'.format(garden_pk)
    if not request.session.get(session_key):
        garden.hits += 1
        garden.save()
        request.session[session_key] = True

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

    context = {
        'garden': garden,
        'comments': comments,
        'comment_form': comment_form,
        'room_name': "broadcast"
    }
    return render(request, 'gardens/detail.html', context)


def search(request):
    query = request.GET.get('query')
    gardens = Garden.objects.filter(title__icontains=query)  
    
    context = {
        'query': query,
        'gardens': gardens,
        'room_name': "broadcast"
    }
    return render(request, 'gardens/search.html', context)