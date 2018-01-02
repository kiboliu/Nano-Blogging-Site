from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.db import transaction

from socialnetwork.models import *
from socialnetwork.forms import RegistrationForm, CreatePostForm, EditProfileForm

import datetime

# Action for the default /socialnetwork/ route.
@login_required
def home(request):
    all_posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    follower = profile.follows
    all_follower_posts = []
    if follower:
        for post in all_posts:
            if post.user.username in follower:
                all_follower_posts.append(post)
    return render(request, 'socialnetwork/globalstream.html',{'posts':all_posts[::-1],'profile':profile,'fposts':all_follower_posts[::-1]})

# Action for the /socialnetwork/add-post route.
@login_required
def add_post(request):
    if request.method == 'GET':
        context = {'form': CreatePostForm()}
        return render(request, 'socialnetwork/globalstream.html', context)

    post = Post(user=request.user,date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    create_post_form = CreatePostForm(request.POST, instance=post)
    if not create_post_form.is_valid():
        context = {'form':create_post_form}
        return render(request, 'socialnetwork/globalstream.html', context)
    create_post_form.save()
    posts = Post.objects.all()
    context = {'form':create_post_form, 'posts':posts[::-1]}
    return render(request, 'socialnetwork/globalstream.html', context)

@login_required
def profile(request, user):
    try:
        errors = []
        posts = Post.objects.filter(user__username=user)
        profile = Profile.objects.get(user__username=user)
        context={'profile':profile, 'posts':posts[::-1], 'errors':errors}
        return render(request, 'socialnetwork/profile.html', context)
    except User.DoesNotExist:
        return render(request, 'socialnetwork/globalstream.html', {})

@login_required
@transaction.atomic
def editProfile(request):
    if request.method == 'GET':
        profile = Profile.objects.get(user=request.user)
        context = {'profile':profile, 'form': EditProfileForm()}
        return render(request, 'socialnetwork/edit-profile.html',context)
    profile = Profile.objects.select_for_update().get(user=request.user)
    form = EditProfileForm(request.POST, request.FILES, instance=profile)
    if not form.is_valid():
        context = {'profile':profile, 'form': EditProfileForm(request.POST)}
        return render(request, 'socialnetwork/edit-profile.html',context)
    profile.content_type = form.cleaned_data['picture'].content_type
    form.save()
    return redirect(reverse('profile',args=[request.user.username]))

@login_required
def get_photo(request, user):
    profile = Profile.objects.get(user__username=user)
    if not profile.picture:
        imageurl = 'socialnetwork/static/socialnetwork/user.png'
        image_data = open(imageurl, "rb").read()
        return HttpResponse(image_data, content_type="image/png")
    return HttpResponse(profile.picture, content_type=profile.content_type)

@login_required
def follow(request, user):
    followee = User.objects.get(username=user)
    profile = Profile.objects.get(user=request.user)
    profile.follows.append(followee.username)
    profile.save()
    return redirect(reverse('home'))

@login_required
def unfollow(request, user):
    followee = User.objects.get(username=user)
    profile = Profile.objects.get(user=request.user)
    profile.follows.remove(followee.username)
    profile.save()
    return redirect(reverse('home'))

@transaction.atomic
def register(request):
    context = {}
    errors = []
    context['errors'] = errors
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/registration.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'socialnetwork/registration.html', context)
    
    new_user = User.objects.create_user(first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'])
    new_user.save()
    new_profile = Profile(user=new_user,
                          first_name=form.cleaned_data['first_name'],
                          last_name=form.cleaned_data['last_name'])
    new_profile.save()
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'])
    
    login(request, new_user)
    return redirect(reverse('home'))