from django.shortcuts import render
from .models import Image
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    images = Image.display_images()
    return render(request, 'home.html', {"images":images})


