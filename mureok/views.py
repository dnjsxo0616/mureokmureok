from django.shortcuts import render, redirect, HttpResponse
from accounts.forms import CustomAuthenticationForm
from gardens.models import Garden
from plants.models import Plant
from supplies.models import Supply
from accounts.models import User
from django.db.models import Q
from channels.layers import get_channel_layer
import json
from django.template import RequestContext

def main(request):
    form = CustomAuthenticationForm
    context = {
        'form': form,
    }
    return render(request, 'main.html', context)


def home(request):
    return render(request, 'home.html', {
        'room_name': "broadcast"
    })


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
            Q(content__icontains=query) | 
            Q(season__icontains=query)
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
        'search_result_supplies': search_result_supplies

    }
    return render(request, 'search.html', context)