from django.shortcuts import render, redirect
from .models import Community, Community_comment
from .forms import CommunityForm, Community_commentForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import User, User_title, User_profile
from django.contrib import messages
from django.core.paginator import Paginator




def index(request):
    communities = Community.objects.all()[::-1]
    need_experts = Community.objects.filter(need_expert=True)[::-1]
    paginator = Paginator(communities, 4)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    content = {
        'communities': communities,
        'need_experts': need_experts,
        'page_obj': page_obj,
    }
    return render(request, 'communities/index.html', content)



@login_required
def create(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.user = request.user
            community.save()

            return redirect('communities:detail', community.pk)
    else:
        form = CommunityForm()
    context = {
        'form' : form,
    }
    return render(request, 'communities/create.html', context)



def detail(request, community_pk):
    community = Community.objects.get(pk=community_pk)
    community_comment_form = Community_commentForm()
    community_comments = community.community_comment_set.all()
    communities = Community.objects.all().order_by('like_users')
   

    session_key = 'community_{}_hits'.format(community_pk)
    if not request.session.get(session_key):
        community.hits += 1
        community.save()
        request.session[session_key] = True

    context ={
        'community' : community,
        'community_comment_form' : community_comment_form,
        'community_comments' : community_comments,
        'communities': communities,
    }
    return render(request,'communities/detail.html', context)



@login_required
def update(request, community_pk):
    community = Community.objects.get(pk=community_pk)
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES, instance=community)
        if form.is_valid():
            form.save()
            return redirect('communities:detail', community.pk)
    else:
        form = CommunityForm(instance=community)
    context = {
        'community':community,
        'form' : form,
    }
    return render(request,'communities/update.html',context)



@login_required
def delete(request,community_pk):
    community = Community.objects.get(pk=community_pk)
    if request.user == community.user:
        community.delete()
    return redirect('communities:index')



@login_required
def community_likes(request, community_pk):
    community = Community.objects.get(pk=community_pk)
    if community.like_users.filter(pk=request.user.pk).exists():
        community.like_users.remove(request.user)
        is_liked = False
    else:
        community.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'like_count': community.like_users.count(),
    }
    return JsonResponse(context)



from django.http import JsonResponse
@login_required
def community_comment_create(request, community_pk):
    community = Community.objects.get(pk=community_pk)
    community_comment_form = Community_commentForm(request.POST)

    if community_comment_form.is_valid():
        community_comment = community_comment_form.save(commit=False)
        community_comment.community = community
        community_comment.user = request.user
        

       
        if not Community_comment.objects.filter(user=request.user, community=community).exists():
            user_profile = User_profile.objects.get(user=request.user)
            user_profile.points += 1
            user_profile.save()
        
        # 칭호 확인 및 업데이트
            titles = User_title.objects.filter(min_points__lte=user_profile.points, max_points__gte=user_profile.points)
            if titles.exists():
                user_profile.title = titles.first()
                user_profile.save()

        community_comment.save()
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': community_comment_form.errors})



@login_required
def community_comment_update(request, community_pk, community_comment_pk):
    community_comment = Community_comment.objects.get(pk=community_comment_pk)
    if request.user == community_comment.user:
        if request.method == 'POST':
            community_comment_form = Community_commentForm(request.POST, instance=community_comment)
            if community_comment_form.is_valid():
                community_comment_form.save()
                return redirect('communities:detail', community_pk)
                # return JsonResponse({'status': 'success'})
        else:
            community_comment_form = Community_commentForm(instance=community_comment)
        context = {
            'community_comment_form': community_comment_form,
            'community_comment': community_comment,
        }
        return render(request, 'communities/detail.html', context)



@login_required
def community_comment_delete(request, community_pk, community_comment_pk):
    community_comment = Community_comment.objects.get(pk=community_comment_pk)
    if request.user == community_comment.user:
        community_comment.delete()

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'})



@login_required
def community_comment_likes(request,product_pk, community_comment_pk):
    community_comment = Community_comment.objects.get(pk=community_comment_pk)
    if community_comment.like_users.filter(pk=request.user.pk).exists():
        community_comment.like_users.remove(request.user)
        c_is_like = False
    else:
        community_comment.like_users.add(request.user)
        c_is_like = True
    c_like_count = community_comment.like_users.count()

    context={
        'c_is_like' :  c_is_like,
        'c_like_count' : c_like_count,
    }

    return JsonResponse(context)


def filter_communities(request, category):
    communities = Community.objects.filter(category=category)[::-1]
    need_experts = Community.objects.filter(category=category).filter(need_expert=True)[::-1]
    paginator = Paginator(communities, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content ={
        'communities':communities,
        'need_experts':need_experts,
        'page_obj': page_obj, 
    }
    return render(request, 'communities/index.html', content)
