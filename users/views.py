from django.contrib import auth
from django.shortcuts import render ,redirect , get_object_or_404 
from django.http import HttpRequest 
from django.core.mail import EmailMessage , EmailMultiAlternatives
from django.template.loader import get_template , render_to_string
from django.utils.html import strip_tags
from .models import Destination , blog_user , Flight
from verify_email.email_handler import send_verification_email
from django.urls import reverse
import stripe
stripe.api_key = "sk_test_51I729tFz1TxC4hZ6UNWmTbdPyCOeqymlf5nzuNdzLVP3Xi1ai2FSsnqSt2Pl3fOo7AxkgisGhtSoLrHpgiaZJcQL00XdgowYVj"

import datetime , math

# To Authenticate

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login as log_in ,logout

#To add Messages
from django.contrib import messages
#To Import User Creation Form

from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm , ContactForm , FlightForm
# Create your views here.

def login(request):
    if request.method=='POST':
        username = request.POST.get('uname')
        password = request.POST.get('pwd')

        user = authenticate(request,username=username,password=password)
        print(user)


        if user is not None:

            log_in(request,user)
            if request.user.is_authenticated:
                messages.success(request, "Login Successfull!")
            return redirect('home')
        else:
            messages.warning(request ,'USERNAME OR PASSWORD IS INCORRECT')
            


    context = {}
    return render(request,"users/login.html",context)



def logoutUser(request):
    logout(request)
    messages.success(request ,'Logged Out Successfully')
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
                send_verification_email(request, form)
                user = form.cleaned_data['username']
                messages.success(request ,'Email sent Successfully Verify it to login' +"   " + user)
                messages.success(request ,'Account Created for' +"   " + user)
                return redirect('login')

        context = {'form':form}
        return render(request,"users/register.html",context)

# @login_required(login_url='login')
def home(request):
    destinations = Destination.objects
    return render(request , "users/index.html",{'destinations': destinations})






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
                ['realtorsapi@gmail.com'],
               headers = {'Reply-To': email }

            )

            email.attach_alternative(html_template, 'text/html')
            email.send()
            messages.success(request ,'Request Sent Successfully')
            return redirect('contact')

    return render(request,'users/contact.html',{'form': form})


def about(request):
    return render(request , 'users/about.html',context={})

@login_required(login_url='login')
def blog(request):
    blogs = blog_user.objects
    return render(request,'users/blog.html',{'blogs': blogs})



@login_required(login_url='login')
def destination_details(request, pk):
    destination_info = get_object_or_404(Destination,pk=pk)
    return render(request,'users/destination_details.html',{'destination_info_detail':destination_info})

@login_required(login_url='login')
def single_blog(request):
    return render(request,'users/single-blog.html',context={})


@login_required(login_url='login')
def travel_destination(request):
    return render(request,'users/travel_destination.html',context={})



@login_required(login_url='login')
def graph(request):
    queryset = Destination.objects
    return render(request, 'users/graphs.html', {'data':queryset})





def flight(request):
    flight_form = FlightForm()
    if request.method == 'POST':
        flight_form = FlightForm(request.POST)
        if flight_form.is_valid():
            source = flight_form.cleaned_data['source']
            sourceArr = source.split(',')
            sourceCity = sourceArr[0].lower()
            destination = flight_form.cleaned_data['destination']
            destinationArr = destination.split(',')
            destinationCity = destinationArr[0].lower()
            startdate = flight_form.cleaned_data['date']
            year = startdate.year
            month = startdate.month
            day = startdate.day
            choice = flight_form.cleaned_data['travel_type']
            if (choice == 'economy'):
                flights = Flight.objects.filter(sourceLocation = sourceCity).filter(destinationLocation=destinationCity).filter(departureDate=datetime.date(year,month,day)).filter(numSeatsRemainingEconomy__gt=0)
                flights = list(flights)
                return render(request, 'users/flights.html',{"results":"yes", "some_list": flights, "class":choice})
            elif (choice == 'business'):
                flights = Flight.objects.filter(sourceLocation = sourceCity).filter(destinationLocation=destinationCity).filter(departureDate=datetime.date(year,month,day)).filter(numSeatsRemainingBusiness__gt=0)
                flights = list(flights)
                return render(request, 'users/flights.html',{"results":"yes", "some_list": flights, "class":choice})
            elif(choice == 'first'):
                flights = Flight.objects.filter(sourceLocation = sourceCity).filter(destinationLocation=destinationCity).filter(departureDate=datetime.date(year,month,day)).filter(numSeatsRemainingFirst__gt=0)
                flights = list(flights)
                return render(request, 'users/flights.html',{"results":"yes", "some_list": flights, "class":choice})
            elif(choice == 'non'):
                return render(request , 'users/flights.html' , {"results":"no"})
    return render(request,'users/flights.html' , {'form1': flight_form})


@login_required(login_url='login')
def payment(request , pk ):
    travel_class = request.GET.get('class')
    booking_details = get_object_or_404(Flight , pk = pk)
    return render(request , 'users/payment.html',{"booking_details": booking_details , "class" : travel_class})


def charge(request):
	
	if request.method == 'POST':
		print('Data:', request.POST)

		amount = float(request.POST['amount'])



		customer = stripe.Customer.create(
			        name = request.POST['nickname'],
			        email = request.POST['email'],
					address = {"city":"mumbai","country":"india","line1":"unr","line2":"thane","postal_code":"421005","state":"maharashtra"},
					source = request.POST['stripeToken']
		             )


		charge = stripe.Charge.create(
			customer = customer,
			amount = round(amount)*100,
			currency = 'inr',
			description = 'Order Payment Received'
		)

	return redirect(reverse('success', args=[amount]))

def successMsg(request, args):
	amount = args
	return render(request, 'users/success.html', {'amount':amount})
    

