from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Image, Like, Comment, Profile, Follows
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    images = Image.display_images()
    return render(request, 'home.html', {"images":images})


@login_required
def search(request):
  if 'search_user' in request.GET and request.GET["search_user"]:
    name = request.GET.get('search_user')
    the_users = Profile.search_profiles(name)
    images = Image.search_images(name)
    print(the_users) 
    return render(request,'search.html',{"users":the_users,"images":images})
  else:
    return render(request,'search.html')


@login_required
def others_profile(request,pk):
  user = User.objects.get(pk = pk)
  images = Image.objects.filter(user = user)

  return render(request,'othersprofile.html',{"user":user,"images":images})