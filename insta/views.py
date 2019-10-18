from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Image, Like, Comment, Profile, Follows
from django.contrib.auth.models import User
from . forms import Registration,UpdateUser,UpdateProfile,CommentForm,postImageForm, NewPostForm
from django.contrib import messages


# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    images = Image.display_images()
    comments = Comment.objects.all()
    users = User.objects.all()
    current_user = request.user
    if request.method == 'POST':
      form = CommentForm(request.POST)
      img_id = request.POST['image_id']
      if form.is_valid():
        comment = form.save(commit=False)
        comment.user = current_user
        image = Image.get_image(img_id)
        comment.image = image
        comment.save()
      return redirect(f'/#{img_id}')
    else:
      form = CommentForm(auto_id=False)
    
    context = {
      "images": images,
      "form": form,
      "comments": comments,
      "users": users
    }
        
    return render(request, 'home.html', context)



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

@login_required
def profile(request):
  current_user = request.user
  images = Image.objects.filter(user_id = current_user.id).all()
  return render(request,'profile.html',{"images":images})


@login_required
def update_profile(request):
  if request.method == 'POST':
    u_form = UpdateUser(request.POST,instance=request.user)
    p_form = UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('profile')
  else:
    u_form = UpdateUser(instance=request.user)
    p_form = UpdateProfile(instance=request.user.profile) 
    
  params = {
    'u_form':u_form,
    'p_form':p_form
  }
  return render(request,'update_profile.html', params)

@login_required(login_url = '/accounts/login/')
def new_post(request):
    
    current_user = request.user
    # userProfile = Profile.objects.filter(user = current_user).first()
    
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = form.save(commit = False)
            userProfile = Profile.objects.filter(user = current_user).first()
            image.image_profile = userProfile
            image.save()
            
            return redirect('/')
        
    else:
        form = NewPostForm()
        
    return render(request, 'posts.html', {'form': form})

def register(request):

   if request.method == 'POST':
      form = Registration(request.POST)
      if form.is_valid():
         form.save()
         username = form.cleaned_data.get('username')
         raw_password = form.cleaned_data.get('password1')
         user = authenticate(username=username, password=raw_password)
         login(request, user)
         user = User.objects.filter
         return redirect('edit_profile')
   else:
      form = Registration()

   context = {
      'form': form
   }

   return render(request, 'registration/registration_form.html', context)



 