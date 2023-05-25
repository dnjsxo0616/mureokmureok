from django.shortcuts import render
from accounts.forms import CustomAuthenticationForm

def main(request):
    form = CustomAuthenticationForm
    context = {
        'form': form,
    }
    return render(request, 'main.html', context)


def home(request):
    return render(request, 'home.html')