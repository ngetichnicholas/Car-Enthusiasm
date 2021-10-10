from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import MessageSerializer
from django.http.response import JsonResponse, HttpResponse




from .models import *
from .forms import *
from .email import *


# Create your views here.
def index(request):
  current_user = request.user
  cars = Car.objects.all()
  
  context = {
    'current_user':current_user,
    'cars':cars
    }
  return render(request, 'index.html',context)

def contact(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    if request.method == 'POST':
      contact_form = ContactForm(request.POST)
      if contact_form.is_valid():
        contact_form.save()
        send_contact_email(name, email)
        data = {'success': 'Your message has been reaceived. Thank you for contacting us, we will get back to you shortly'}
        messages.success(request, f"Message submitted successfully")
    else:
      contact_form = ContactForm()
    return render(request,'contact.html',{'contact_form':contact_form})

def signup_view(request):
    if request.method=='POST':
        signup_form=UserSignUpForm(request.POST)
        if signup_form.is_valid():
            user=signup_form.save()
            user.refresh_from_db()
            return redirect('login')
    else:
        signup_form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'signup_form': signup_form})

def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        auth_login(request, user)
        messages.info(request, f"You are now logged in as {username}")
        return redirect('index')

      else:
        messages.error(request, "Invalid username or password.")
    else:
      messages.error(request, "Invalid username or password.")
  form = AuthenticationForm()
  return render(request = request,template_name = "registration/login.html",context={"form":form})

def car_view(request,car_id):
  current_user = request.user
  car = Car.objects.get(pk = car_id)
  
  return render(request, 'cars/car_page.html', {'current_user':current_user,'car':car})

@login_required
def profile(request):
  current_user = request.user

  return render(request,'profile/profile.html',{"current_user":current_user})

@login_required
def update_profile(request):
  if request.method == 'POST':
    user_form = UpdateUserForm(request.POST,request.FILES,instance=request.user)
    if user_form.is_valid():
      user_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('profile')
  else:
    user_form = UpdateUserForm(instance=request.user)
  params = {
    'user_form':user_form,
  }
  return render(request,'profile/update.html',params)

@login_required
def add_car(request):
  if request.method == 'POST':
    add_car_form = CarForm(request.POST,request.FILES)
    if add_car_form.is_valid():
      car = add_car_form.save(commit=False)
      car.user_id = request.user
      car.save()
      messages.success(request, f'New car added!')
      return redirect('index')

  else:
    add_car_form = CarForm()
    
  return render(request, 'cars/add_car.html',{'add_car_form':add_car_form})

@login_required
def cars(request):
  cars = Car.objects.filter(user_id = request.user.id).order_by('-model')
  return render(request,'cars/cars.html',{'cars':cars})

@login_required
def update_car(request, car_id):
  car = Car.objects.get(pk=car_id)
  if request.method == 'POST':
    update_car_form = CarForm(request.POST,request.FILES, instance=car)
    if update_car_form.is_valid():
      update_car_form.save()
      messages.success(request, f'car updated!')
      return redirect('cars')
  else:
    update_car_form = CarForm(instance=car)
  context = {
      "update_car_form":update_car_form,
      "car":car
  }
  return render(request, 'cars/update_car.html', context)

@login_required
def delete_car(request,car_id):
  car = Car.objects.get(pk=car_id)
  if car:
    car.delete_car()
    messages.success(request, f'car deleted!')
  return redirect('cars')

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})

def search(request):
  if 'car' in request.GET and request.GET["car"]:
    search_term = request.GET.get("car")
    searched_cars = Car.search_cars(search_term)
    message = f"{search_term}"

    return render(request,'search.html', {"message":message,"cars":searched_cars})

  else:
    message = "You haven't searched for any term"
    return render(request,'search.html',{"message":message})