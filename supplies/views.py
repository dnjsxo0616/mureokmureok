from django.shortcuts import render, redirect
from .models import Supply
from .forms import SupplyForm
from taggit.models import Tag
from django.contrib.auth.decorators import login_required

# Create your views here.



def supply_index(request):
    supplies = Supply.objects.all()[::-1]
    content = {
        'supplies': supplies,
    }
    return render(request, 'supplies/index.html', content)



@login_required
def supply_create(request):
    if request.method == 'POST':
        tags = request.POST.get('tags').split(',')
        form = SupplyForm(request.POST, request.FILES)
        if form.is_valid():
            supply = form.save(commit=False)
            supply.user = request.user
            supply.save()
            for tag in tags:
                supply.tags.add(tag.strip())
            return redirect('supplies:supply_detail', supply.pk)
    else:
        form = SupplyForm()
    context = {
        'form' : form,
    }
    return render(request, 'supplies/create.html', context)



def supply_detail(request, supply_pk):
    supply = Supply.objects.get(pk=supply_pk)
    tags = supply.tags.all()
    supplies = Supply.objects.all().order_by('like')

    session_key = 'supply_{}_hits'.format(supply_pk)
    if not request.session.get(session_key):
        supply.hits += 1
        supply.save()
        request.session[session_key] = True

    context ={
        'supply' : supply,
        'tags': tags,
        'supplies': supplies,
    }
    return render(request,'supplies/detail.html', context)



def supply_delete(request, supply_pk):
    supply = Supply.objects.get(pk=supply_pk)
    if request.user == supply.user:
        supply.delete()
    return redirect('supplies:index')



def supply_update(request):
    supply = Supply.objects.get(pk=supply_pk)
    if request.method == 'POST':
        form = SupplyForm(request.POST, request.FILES, instance=supply)
        if form.is_valid():
            tags = request.POST.get('tags').split(',')
            for tag in tags:
                supply.tags.add(tag.strip())
            form.save()
            return redirect('supplies:detail', supply.pk)
    else:
        form = SupplyForm(instance=supply)
    context = {
        'supply':supply,
        'form' : form,
    }
    return render(request,'supplies/update.html',context)

def likes(request, supply_pk):
    supply = Supply.objects.get(pk=supply_pk)
    if supply.like_users.filter(pk=request.user.pk).exists():
        supply.like_users.remove(request.user)
        is_liked = False
    else:
        supply.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'like_count': supply.like_users.count(),
    }
    return JsonResponse(context)












def filter_supplies(request):
    selected_tags = request.GET.getlist('tags')
    supplies = Supply.objects.filter(tags__in=selected_tags)
    context = {'supplies': supplies, 'selected_tags': selected_tags}
    return render(request, 'filter_supplies.html', context)
