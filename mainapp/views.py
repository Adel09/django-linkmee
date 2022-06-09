from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Link, Page
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import LinkSerializer, PageSerializer

# Create your views here.
def home(request):
    context = {'title': 'Your Personal Link Directory | LinkMe'}
    return render(request, 'index.html', context)

def signupuser(request):
    if request.method == 'GET':
        context = {'title': 'Create your account | LinkMe'}
        return render(request, 'signup.html', context)
    else:
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                user = User.objects.create_user(email=request.POST['email'],username=request.POST['username'], password=request.POST['pass1'])
                user.save()
                page = Page.objects.create(name=request.POST['pagename'], bio=request.POST['about'], owner=user)
                page.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                context = {'title': 'Create your account| Crummy Files',
                            'error' : 'User already registered'}
                return render(request, 'signup.html', context)
        else:
            context = {'title': 'Create your account| Crummy files',
                            'error' : 'Passwords do not match'}
            return render(request, 'signup.html', context)


def signinuser(request):
    if request.method == 'GET':
        context = {'title' : "Log into your dashboard | LinkMe"}
        return render(request, 'login.html', context)
        
    else:
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            context = {'title': 'Log into your dashboard | LinkMe',
                            'error' : 'Please check your username/password'}
            return render(request, 'signup.html', context)

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def dashboard(request):
    user = User.objects.get(username=request.user)
    page = Page.objects.get(owner = user)
    links = Link.objects.filter(page = page)
    
    context = {'title': 'My Links | LinkMe',
                    'user': user,
                    'page': page,
                    'links' : links}
    return render(request, 'dash.html', context)


def addlink(request):
    if request.method == 'GET':
        context = {'title' : 'Add a new link to your page'}
        return render(request, 'add-link.html', context)
    else:
        title = request.POST['title']
        url = request.POST['url']
        page = Page.objects.get(owner=request.user)
        link = Link.objects.create(title=title, url=url, page=page)
        link.save()
        return redirect('dashboard')

def testpage(request):
    context = {'title' : 'Test Page'}
    return render(request, 'test.html', context)

def viewpage(request, username):
    user = User.objects.get(username=username)
    page = Page.objects.get(owner=user)
    links = Link.objects.filter(page=page)
    context = {'title' : f'{page.name} Links',
                'page' : page,
                'links' : links}
    return render(request, 'viewpage.html', context)

def delete(request, id):
    if request.method == 'POST':
        link = Link.objects.get(id=id)
        link.delete()
        return redirect(dashboard)
    
# def allLinks(request):
#     links = Link.objects.all()
#     serializer = LinkSerializer(links, many=True)
#     return JsonResponse(serializer.data, safe=False)