from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from mainapp.models import Link, Page
from .serializers import LinkSerializer, PageSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token

# Create your views here.
@api_view(['post'])
@csrf_exempt
def registeruser(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(email=request.data['email'],username=request.data['username'], password=request.data['pass'])
            user.save()
            page = Page.objects.create(name=request.data['pagename'], bio=request.data['about'], owner=user)
            page.save()
            token = Token.objects.create(user=user)
            login(request, user)
            responsee = {
                "token" : token.key,
            }
            
            return JsonResponse(responsee, safe=False, status=200)
        except IntegrityError:
            res = {"message" : "User already exists"}
            return JsonResponse(res, status=401)
        
    else:
        res = {"message" : "Invalid request method"}
        return JsonResponse(res, status=401)

@api_view(['post'])
@csrf_exempt
def loginuser(request):
    if request.method == 'POST':
        username = request.data["username"]
        password = request.data['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                token = Token.objects.create(user=user)
                print(token.key)
                res = {"token" : f"{token.key}"}
                login(request, user)
                return JsonResponse(res, status=200)
            except IntegrityError:
                token = Token.objects.get(user=user)
                print(token.key)
                res = {"token" : f"{token.key}"}
                return JsonResponse(res, status=200)
        else:
            res = {"message" : "Invalid data"}
            return JsonResponse(res, status=401)

@api_view(['GET'])
def getMyLinks(request):
    if request.user.is_authenticated:
        user = request.user
        page = Page.objects.get(owner=user)
        links = Link.objects.filter(page=page)
        serializer = LinkSerializer(links, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    else:
        res = {"message" : "You're not authenticated"}
        return JsonResponse(res, status=401)

@api_view(['GET'])
def getMyPage(request):
    if request.user.is_authenticated:
        user = request.user
        page = Page.objects.get(owner=user)
        serializer = PageSerializer(page)
        return JsonResponse(serializer.data, safe=False, status=200)
    else:
        res = {"message" : "You're not authenticated"}
        return JsonResponse(res, status=401)


@api_view(['GET'])
def getUser(request):
    if request.user.is_authenticated:
        user = request.user
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    else:
        res = {"message" : "You're not authenticated"}
        return JsonResponse(res, status=401)

@api_view(['POST'])
def addLink(request):
    if request.user.is_authenticated:
        title = request.data['title']
        url = request.data['url']
        page = Page.objects.get(owner=request.user)
        link = Link.objects.create(title=title, url=url, page=page)
        link.save()
        res = {
            'status' : 'success',
            'message' : 'Link added successfully'
        }
        return JsonResponse(res, status=201)
    else:
        res = {"message" : "You're not authenticated"}
        return JsonResponse(res, status=401)

@api_view(['POST'])
def updatebio(request):
    if request.user.is_authenticated:
        bio = request.data['bio']
        page = Page.objects.get(owner=request.user)
        page.bio = bio
        page.save(update_fields=['bio'])
        # link = Link.objects.create(title=title, url=url, page=page)
        # link.save()

        res = {
            'status' : 'success',
            'message' : 'Bio updated successfully'
        }
        return JsonResponse(res, status=201)
    else:
        res = {"message" : "You're not authenticated"}
        return JsonResponse(res, status=401)



