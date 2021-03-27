from django.contrib import auth
from django.shortcuts import render , redirect
from django.http import HttpRequest
from django.core.mail import EmailMessage , EmailMultiAlternatives
from django.template.loader import get_template , render_to_string
from django.utils.html import strip_tags


# To Authenticate

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login as log_in ,logout

#To add Messages
from django.contrib import messages
#To Import User Creation Form

from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm , ContactForm
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
    form = ContactForm
    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['message']
            html_template = render_to_string("users/contact_template.html",{'name': name , 'email': email , 'content': content})
            text_content = strip_tags(html_template)

            email = EmailMultiAlternatives(
                "New contact form submission",
                text_content,
                "Travelo" +'',
                ['adityakhandelwal0033@gmail.com'],
               headers = {'Reply-To': email }

            )

            email.attach_alternative(html_template, 'text/html')
            email.send()

            return redirect('contact')

    return render(request,'users/contact.html',{'form': form})


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