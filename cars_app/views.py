from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


from .models import *
from .forms import *
from .email import *


# Create your views here.
def index(request):
  current_user = request.user
  groceries = Car.objects.all()
  
  context = {
    'current_user':current_user,
    'groceries':groceries
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
  
  return render(request, 'car_page.html', {'current_user':current_user,'car':car})