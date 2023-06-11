from django.shortcuts import render, redirect
from .models import Notice
from .forms import NoticeForm
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.models import User, User_title, User_profile
from django.contrib.auth.decorators import login_required


def index(request):
    notices = Notice.objects.all()[::-1]
    paginator = Paginator(notices, 10)
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    content = {
        'notices': notices,
        'page_obj': page_obj,
        'room_name': "broadcast",
    }
    return render(request, 'notices/index.html', content)


@login_required
def create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()

            return redirect('notices:detail', notice.pk)
    else:
        form = NoticeForm()
    context = {
        'form' : form,
        'room_name': "broadcast"
    }
    return render(request, 'notices/create.html', context)


def detail(request, notice_pk):
    notice = Notice.objects.get(pk=notice_pk)


    session_key = 'notice_{}_hits'.format(notice_pk)
    if not request.session.get(session_key):
        notice.hits += 1
        notice.save()
        request.session[session_key] = True

    context ={
        'notice' : notice,
        'room_name': "broadcast"
    }
    return render(request,'notices/detail.html', context)


@login_required
def update(request, notice_pk):
    notice = Notice.objects.get(pk=notice_pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notices:detail', notice.pk)
    else:
        form = NoticeForm(instance=notice)
    context = {
        'notice':notice,
        'form' : form,
        'room_name': "broadcast"
    }
    return render(request,'notices/update.html',context)


@login_required
def delete(request,notice_pk):
    notice = Notice.objects.get(pk=notice_pk)
    if request.user == notice.user:
        notice.delete()
    return redirect('notices:index')