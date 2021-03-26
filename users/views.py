from django.contrib import auth
from django.shortcuts import render , redirect
from django.http import HttpRequest

# To Authenticate

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login as log_in ,logout

#To add Messages
from django.contrib import messages
#To Import User Creation Form

from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm
# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method=='POST':
            username = request.POST.get('uname')
            password = request.POST.get('pwd')

            user = authenticate(request,username=username,password=password)


            if user is not None:
                log_in(request,user)
                return redirect('home')
            else:
                messages.success(request ,'USERNAME OR PASSWORD IS INCORRECT')
                


        context = {}
        return render(request,"users/login.html",context)



def logoutUser(request):
    logout(request)
    return redirect('login')



def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data['username']
                messages.success(request ,'Account Created for' +"   " + user)
                return redirect('login')

        context = {'form':form}
        return render(request,"users/register.html",context)

@login_required(login_url='login')
def home(request):
    return render(request , "users/index.html")


def contact(request):
    return render(request,'users/contact.html',context={})


def about(request):
    return render(request , 'users/about.html',context={})


def blog(request):
    return render(request,'users/blog.html',context={})




def destination_details(request):
    return render(request,'users/destination_details.html',context ={})


def single_blog(request):
    return render(request,'users/single-blog.html',context={})



def travel_destination(request):
    return render(request,'users/travel_destination.html',context={})