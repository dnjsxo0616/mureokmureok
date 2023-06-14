from django.shortcuts import render, redirect, HttpResponse
from accounts.forms import CustomAuthenticationForm
from gardens.models import Garden
from plants.models import Plant
from supplies.models import Supply
from accounts.models import User
from django.db.models import Q, Max
from channels.layers import get_channel_layer
import json
from django.template import RequestContext
from django.db.models import Count
from sales.models import Product
from managements.models import Management

def main(request):
    form = CustomAuthenticationForm
    context = {
        'form': form,
        'room_name': "broadcast"
    }
    return render(request, 'main.html', context)


def home(request):
    popular_plants = Plant.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]
    popular_product = Product.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:4]
    recommended_gardens = Garden.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:1]
    additional_garden_links = Garden.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[1:7]
    recent_plants = Plant.objects.annotate(max_id=Max('id')).order_by('-max_id')
    recent_tags = recent_plants.distinct().values_list('tags__name', flat=True)[:5]
    
    latest_management = Management.objects.filter(user=request.user).latest('managementdate') if request.user.is_authenticated and Management.objects.filter(user=request.user).exists() else None

    context = {
        'room_name': "broadcast",
        'popular_plants': popular_plants,
        'popular_product': popular_product,
        'recommended_gardens': recommended_gardens,
        'additional_garden_links': additional_garden_links,
        'recent_tags': recent_tags,
        'latest_management': latest_management,
    }

    return render(request, 'home.html', context)


from asgiref.sync import async_to_sync
def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "alarm_broadcast",
        {
            'type': 'send_alarm',
            'message': json.dumps("Alarm")
        }
    )
    return HttpResponse("Done")


def search(request):
    query = request.GET.get('q', '')
    if query:
        search_gardens = Garden.objects.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query) 
        )
  
        search_plants = Plant.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

        search_supplies = Supply.objects.filter(
            Q(supply_name__icontains=query) |
            Q(category__icontains=query) | 
            Q(price__icontains=query)
        )

        search_result_gardens = list(search_gardens)
        search_result_plants = list(search_plants)
        search_result_supplies = list(search_supplies)
       
    else:
        search_result_gardens = list(Garden.objects.all())
        search_result_plants = list(Plant.objects.all())
        search_result_supplies = list(Supply.objects.all())
    context = {
        'search_result_gardens': search_result_gardens,
        'search_result_plants': search_result_plants,
        'search_result_supplies': search_result_supplies,
        'query': query,
    }
    return render(request, 'search.html', context)