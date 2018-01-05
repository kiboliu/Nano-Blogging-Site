from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.db import transaction

from django.views.decorators.csrf import ensure_csrf_cookie

from socialnetwork.models import *
from socialnetwork.forms import RegistrationForm, CreatePostForm, EditProfileForm

import datetime
import json
import ast

# Action for the default /socialnetwork/ route.
@login_required
@ensure_csrf_cookie
def home(request):
    all_posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    follower = profile.follows
    all_follower_posts = []
    follower_ids = []
    if follower:
        for post in all_posts:
            if post.user.username in follower:
                all_follower_posts.append(post)
    return render(request, 'socialnetwork/globalstream.html',{'posts':all_posts[::-1],'profile':profile,'fposts':all_follower_posts[::-1]})

@login_required
@ensure_csrf_cookie
def get_post(request):
    posts = Post.objects.all()
    response_text = serializers.serialize('json', posts)
    response_text = json.loads(response_text)
    response = "["
    for post in response_text:
        comment_list = serializers.serialize('json', Comment.objects.filter(post__id=post['pk']))
        comment_list = json.loads(comment_list)
        post['comments'] = comment_list
        post = json.dumps(post)
        response = response + post + ", "
    response = response[:-2] + "]"
    return HttpResponse(response, content_type='application/json')

# Action for the /socialnetwork/add-post route.
@login_required
@ensure_csrf_cookie
def add_post(request):
    # if request.method == 'GET':
    #     context = {'form': CreatePostForm()}
    #     return render(request, 'socialnetwork/globalstream.html', context)

    # post = Post(user=request.user,date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # create_post_form = CreatePostForm(request.POST, instance=post)
    # if not create_post_form.is_valid():
    #     context = {'form':create_post_form}
    #     return render(request, 'socialnetwork/globalstream.html', context)
    # create_post_form.save()
    # posts = Post.objects.all()
    # context = {'form':create_post_form, 'posts':posts[::-1]}
    # return render(request, 'socialnetwork/globalstream.html', context)
    errors = []
    if not 'content' in request.POST or not request.POST['content']:
        message = 'You muste enter a post.'
        json_error = '{"error":"'+message+'"}'
        return HttpResponse(json_error,content_type='application/json')
    new_post = Post(user=request.user,date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),content=request.POST['content'])
    new_post.save()
    return redirect(reverse('getpost'))

@login_required
@ensure_csrf_cookie
def add_comment(request):
    errors = []
    if not 'comment' in request.POST or not request.POST['comment']:
        message = 'You muste enter a comment.'
        json_error = '{"error":"'+message+'"}'
        return HttpResponse(json_error,content_type='application/json')
    print(request.POST['postid'])
    related_post=Post.objects.get(id=int(request.POST['postid']))
    new_comment = Comment(user=request.user,time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),content=request.POST['comment'],post=related_post)
    new_comment.save()
    return redirect(reverse('getpost'))
    
@login_required
@ensure_csrf_cookie
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
@ensure_csrf_cookie
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
    if form.cleaned_data['picture'].content_type.startWith('img'):
        profile.content_type = form.cleaned_data['picture'].content_type
    form.save()
    return redirect(reverse('profile',args=[request.user.username]))

@login_required
@ensure_csrf_cookie
def get_photo(request, user):
    profile = Profile.objects.get(user__username=user)
    if not profile.picture:
        imageurl = 'socialnetwork/static/socialnetwork/user.png'
        image_data = open(imageurl, "rb").read()
        return HttpResponse(image_data, content_type="image/png")
    return HttpResponse(profile.picture, content_type=profile.content_type)

@login_required
@ensure_csrf_cookie
def follow(request, user):
    followee = User.objects.get(username=user)
    profile = Profile.objects.get(user=request.user)
    profile.follows.append(followee.username)
    profile.save()
    return redirect(reverse('home'))

@login_required
@ensure_csrf_cookie
def unfollow(request, user):
    followee = User.objects.get(username=user)
    profile = Profile.objects.get(user=request.user)
    profile.follows.remove(followee.username)
    profile.save()
    return redirect(reverse('home'))

@transaction.atomic
@ensure_csrf_cookie
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