from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm, UserForm

# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
       return redirect('home') 

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) # This is what authenticates the user. It assigns a session ID in the browser
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request) #removes the assigned session from the user
    return redirect('home')


def registerUser(request):
   form = UserCreationForm()
   if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "Your account was created successfully! 🎉")
            return redirect('home')
        else:
            # Loop through form errors and display them as flash messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

   return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0: 5]
    room_count = room.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #This will filter the recent activity by the topic that has been selected
    context = {'rooms': room, 'topics':topics, 'room_count': room_count, 'room_messages' : room_messages }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all() #For many to one relationship, you have to use '_set' when establishing the function but for ManytoMany, you do not use the '_set' function

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user   # assign logged-in user
            message.room = room           # assign the room
            message.save()
            room.participants.add(request.user) #If join functionality is not added, add it yourself
            return redirect('room', pk=room.id)# The code can work without this but to maintain some functionality working, its best to use this way
    else:
        form = MessageForm()

    context = {
        'room': room,
        'room_messages': room_messages,
        'form': form,
        'participants':participants
    }
    return render(request, 'base/room.html', context)





def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)






@login_required(login_url='login')# Assigns permissions based on session status(reflected in frontend)
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)




@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    #the instance will take the current data in the various fields and prefill the fields with those values so that they can be edited.
    # Then it will take the edited values and replace those in the the instance with it for it to become the most current 
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Caution! only hosts can update rooms')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def updateUser(request):
    user = request.user
    # Prepopulate the about field from last_name
    form = UserForm(instance=user, initial={'about': user.last_name})

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            about_text = form.cleaned_data.get('about')
            user.last_name = about_text
            user.save()

            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form, 'user': user})








@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Caution! only hosts can delete rooms')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
        


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('Caution! only hosts can delete message')
    
    room_id = message.room.id
    
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=room_id)
    return render(request, 'base/delete.html', {'obj':message})


'''@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})'''


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    return render(request, 'base/topics.html', {'topics': topics})
#Find ways to organize the topics by value inside their side of the panel


def activitiesPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})