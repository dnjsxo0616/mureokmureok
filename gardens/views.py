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
    garden = Garden.objects.get(pk=garden_pk)
    if request.user == garden.user:
        garden.delete()
    return redirect('garden:index')


def comment(request,garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    comment_form = CommentForm(request.POST,request.FILES)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.garden = garden
        comment.user = request.user
        comment.save()
        return redirect('gardens:detail', garden_pk)
    context = {
        'garden': garden,
        'comment_form': comment_form,
    }
    return render(request, 'gardens/comment.html', context)

def comment_delete(request, product_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('products:detail', product_pk)


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


def like_garden(request,garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    if garden.like_user.filter(pk=request.user.pk).exists():
        garden.like_user.remove(request.user)
    else:
        garden.like_user.add(request.user)
    return redirect('gardens:detail', garden_pk)


def listing(request):
    category = request.GET.get('category')
    gardens = Garden.objects.filter(category=category)

    context = {
        'category': category,
        'gardens': gardens,
    }
    return render(request, 'gardens/listing.html', context)


def detail(request, garden_pk):
    garden = Garden.objects.get(pk=garden_pk)
    comments = garden.comments.all()

    comment_comment_form = []
    for comment in comments:
        comment_form = CommentForm(instance=comment)
        comment_comment_form.append((comment, comment_form))

    context = {
        'garden': garden,
        'comment_comment_form': comment_comment_form,
    }
    return render(request, 'gardens/detail.html', context)


def location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        garden = Garden(latitude=latitude, longitude=longitude)
        garden.save()

        return redirect('gardens:detail', garden.pk)

    return render(request, 'gardens/location.html')
