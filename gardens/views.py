from django.shortcuts import render,redirect

from .forms import GardenForm, CommentForm
from .models import Garden, Comment


# Create your views here.
def create(request):
    if request.method == 'POST':
        form = GardenForm(request.POST, request.FILES)
        if form.is_valid():
            fo = form.save(commit=False)
            fo.user = request.user
            fo.save()
            return redirect('gardens:index')
        else:
            print(form.errors)
    else:
        form = GardenForm()
    context = {
        'form': form,
    }
    return render(request, 'gardens/create.html', context)



def delete(request, garden_pk):
    garden = garden.objects.get(pk=garden_pk)
    if request.user == garden.user:
        garden.delete()
    return redirect('garden:index')


# def comment(request,garden_pk):
#     garden = Garden.objects.get(pk=garden_pk)
#     comment_form = CommentForm(request.POST,request.FILES)

#     if comment_form.is_valid():
#         comment = comment_form.save(commit=False)
#         comment.garden = garden
#         comment.user = request.user
#         comment.save()
#         return redirect('gardens:detail', garden_pk)
#     context = {
#         'garden': garden,
#         'comment_form': comment_form,
#     }
#     return render(request, 'gardens/comment.html', context)


def update(request, garden_pk):
    garden = Garden.objects.get(pk=garden_pk)

    if request.method == 'POST':
        form = GardenForm(request.POST, request.FILES, instance=garden)
        if form.is_valid():
            form.save()
            return redirect('gardens:index')
        else:
            print(form.errors)
    else:
        form = GardenForm(instance=garden)
    
    context = {
        'form': form,
    }
    return render(request, 'gardens/create.html', context)



def like_garden(request,garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    if garden.like_users.filter(pk=request.user.pk).exists():
        garden.like_users.remove(request.user)
    else:
        garden.like_users.add(request.user)
    return redirect('gardens:detail', garden_pk)

def listing(request):
    gardens = Garden.objects.all()
    context = {
        'gardens': gardens,
    }
    return render(request, 'gardens/listing.html', context)
