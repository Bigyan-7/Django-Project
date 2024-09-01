from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from .forms import RoomForm
from .models import Room,Topic
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect

# Create your views here.

# rooms=[

#     {'id':1, 'name':"Let's Learn Python"},
#     {'id':2, 'name':"Design With Me!"},
#     {'id':3, 'name':"Frontend Developers"},
   

# ]


def loginPage(request):

    page='login'

    if request.method == 'POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')


        try:
            user=User.objects.get(username=username)

        except:
            messages.error(request,"User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    
        else:
            messages.error(request,"Username or password doesn't match.")


    context={'page':page}
    return render(request,'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    # page='register'
    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request,'Could not register! Please retry.')

    return render(request,'base/login_register.html',{'form':form})


def home(request):
    # return HttpResponse('Home Page')
    topics=Topic.objects.all()
    rooms=Room.objects.all()
    context={'rooms':rooms,'topics':topics}
    return render(request,'base/home.html',context)


def room(request,pk):
    # return HttpResponse('Room')

    # room=None
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room=i

    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request,'base/room.html',context)


def createRoom(request):
    form=RoomForm()

    if request.method == 'POST':
        # print(request.POST) # shows the data from website
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request, 'base/room_form.html',context)


def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.method == 'POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)


def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj':room})


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    context={'user':user,'rooms':rooms}
    return render(request,'base/profile.html',context)