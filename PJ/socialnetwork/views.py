from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.db import transaction

from socialnetwork.models import *

import datetime

# Action for the default /socialnetwork/ route.
@login_required
def home(request):
    all_posts = Post.objects.all()
    return render(request, 'socialnetwork/globalstream.html',{'posts':all_posts[::-1]})

# Action for the /socialnetwork/add-post route.
@login_required
def add_post(request):
    errors = []
    if request.method == 'GET':
        return render(request, 'socialnetwork/globalstream.html', {})
    if 'addpost' not in request.POST or not request.POST['addpost']:
        errors.append('You must enter a post to add.')
    else:
        new_post = Post(content=request.POST['addpost'],
                        user=request.user,
                        date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        new_post.save()
    posts = Post.objects.all()
    context = {'posts':posts[::-1], 'errors':errors}
    return render(request, 'socialnetwork/globalstream.html', context)

@login_required
def profile(request, user):
    errors = []
    posts = Post.objects.filter(user__username=user)
    this_user = User.objects.get(username=user)
    context={'user':this_user, 'posts':posts[::-1], 'errors':errors}
    return render(request, 'socialnetwork/profile.html', context)

@transaction.atomic
def register(request):
    context = {}
    errors = []
    context['errors'] = errors
    if request.method == 'GET':
        return render(request, 'socialnetwork/registration.html', context)
    
    if not 'firstname' in request.POST or not request.POST['firstname']:
        errors.append('First Name is required.')
    else:
        context['firstname'] = request.POST['firstname']

    if not 'lastname' in request.POST or not request.POST['lastname']:
        errors.append('Last Name is required.')
    else:
        context['lastname'] = request.POST['lastname']

    if not 'username' in request.POST or not request.POST['username']:
        errors.append('User Name is required.')
    else:
        context['username'] = request.POST['username']
    
    if not 'password' in request.POST or not request.POST['password']:
        errors.append('Password is required.')
    if not 'password-confirm' in request.POST or not request.POST['password-confirm']:
        errors.append('Confirm password is required.')
    
    if errors:
        # Required fields are missing.  Display errors, now.
        return render(request, 'socialnetwork/registration.html', context)
    
    if request.POST['password'] != request.POST['password-confirm']:
        errors.append('Passwords did not match.')

    if User.objects.select_for_update().filter(username = request.POST['username']).exists():
        errors.append('Username is already taken.')

    if errors:
        # Required fields are missing.  Display errors, now.
        return render(request, 'socialnetwork/registration.html', context)
    
    new_user = User.objects.create_user(first_name=request.POST['firstname'],
                                        last_name=request.POST['lastname'],
                                        username=request.POST['username'],
                                        password=request.POST['password'])
    new_user.save()
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
    
    login(request, new_user)
    return redirect('/socialnetwork/')