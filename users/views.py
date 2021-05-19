from users.utils import estimate_coef, get_plot, get_plot1
from django.contrib import auth
from django.http.response import HttpResponse
from django.shortcuts import render ,redirect , get_object_or_404 
from django.http import HttpRequest 
from django.core.mail import EmailMessage , EmailMultiAlternatives
from django.template.loader import get_template , render_to_string
from django.utils.html import strip_tags
from django.contrib.sessions.models import Session
from stripe.api_resources import source
from .models import Destination , blog_user , Flight , Train , Hotel , History_Flight , History_Train , History_Package , History_Hotel
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

from .forms import BlogForm, CreateUserForm , ContactForm , FlightForm , TrainForm , HotelForm
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
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_desc = form.cleaned_data['blog_desc']
            blog_heading = form.cleaned_data['blog_heading']
            blog_image = form.cleaned_data['blog_image']
            blog_date = form.cleaned_data['blog_date']
            user = request.user
            print(blog_desc , blog_heading ,blog_image , blog_date)
            obj = blog_user.objects.create(blog_image = blog_image , blog_heading = blog_heading , blog_desc = blog_desc , blog_date = blog_date , createdBy = str(user))
            obj.save()
        else:
            print("Arre gand mara gaye bhai")
            

    blogs = blog_user.objects.order_by('-pk')
    length = blog_user.objects.order_by('-pk').count()
    return render(request,'users/blog.html',{'blogs': blogs, 'form': form, 'length': length})



@login_required(login_url='login')
def destination_details(request, pk):
    book_type = 'Package'
    book_class = 'package'
    destination_info = get_object_or_404(Destination,pk=pk)
    destinations = Destination.objects
    return render(request,'users/destination_details.html',{'destination_info_detail':destination_info, 'destinations': destinations , "book_type": book_type , "class": book_class})

@login_required(login_url='login')
def single_blog(request):
    return render(request,'users/single-blog.html',context={})


@login_required(login_url='login')
def travel_destination(request):
    return render(request,'users/travel_destination.html',context={})


@login_required(login_url='login')
def graph(request):
    if request.user.is_superuser == True:
        queryset = Destination.objects.all()
        flights = Flight.objects.all()
        trains = Train.objects.all()
        hotels = Hotel.objects.all()
        x_flight = [int(x.fareFirst) for x in flights]
        y_flight = [int(y.fareEconomy) for y in flights]

        x_train = [int(x.fareFirst) for x in trains]
        y_train = [int(y.fareEconomy) for y in trains]

        b = estimate_coef(x_flight , y_flight)


        chart = get_plot(x_flight , y_flight , b)
        chart1 = get_plot(x_train , y_train , b)
        chart2 = get_plot1(x_flight , y_flight)
        chart3 = get_plot1(x_train , y_train)





        return render(request, 'users/graphs.html', {'data':queryset , 'chart': chart, 'chart1':chart1, 'chart2': chart2, 'chart3':chart3 })
    else:
        return redirect('home')


@login_required(login_url='login')
def history(request):
    user = request.user
    history_flight = History_Flight.objects.filter(user=user)
    history_train = History_Train.objects.filter(user = user)
    history_package = History_Package.objects.filter(user = user)
    history_hotel = History_Hotel.objects.filter(user = user)
    return render(request,'users/history.html' , {"history_flight": history_flight ,"history_train":history_train , "history_package":history_package,"history_hotel":history_hotel})



def flight(request):
    flight_form = FlightForm()
    if request.method == 'POST':
        flight_form = FlightForm(request.POST)
        if flight_form.is_valid():
            book_type = 'Flight'
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
                return render(request, 'users/flights.html',{"results":"yes", "book_type": book_type , "some_list": flights, "class":choice})
            elif (choice == 'business'):
                flights = Flight.objects.filter(sourceLocation = sourceCity).filter(destinationLocation=destinationCity).filter(departureDate=datetime.date(year,month,day)).filter(numSeatsRemainingBusiness__gt=0)
                flights = list(flights)
                return render(request, 'users/flights.html',{"results":"yes", "book_type": book_type , "some_list": flights, "class":choice})
            elif(choice == 'first'):
                flights = Flight.objects.filter(sourceLocation = sourceCity).filter(destinationLocation=destinationCity).filter(departureDate=datetime.date(year,month,day)).filter(numSeatsRemainingFirst__gt=0)
                flights = list(flights)
                return render(request, 'users/flights.html',{"results":"yes","book_type": book_type , "some_list": flights, "class":choice})
            elif(choice == 'non'):
                return render(request , 'users/flights.html' , {"results":"no"})
    return render(request,'users/flights.html' , {'form1': flight_form})


def train(request):
    train_form = TrainForm()
    if request.method == 'POST':
        train_form = TrainForm(request.POST)
        if train_form.is_valid():
            book_type = 'Train'
            source = train_form.cleaned_data['source']
            sourceArr = source.split(',')
            sourceCity = sourceArr[0].lower()
            destination = train_form.cleaned_data['destination']
            destinationArr = destination.split(',')
            destinationCity = destinationArr[0].lower()
            startdate = train_form.cleaned_data['date']
            year = startdate.year
            month = startdate.month
            day = startdate.day
            choice = train_form.cleaned_data['travel_type']
            if (choice == 'economy'):
                trains = Train.objects.filter(sourceLocation = sourceCity).filter(destinationLocation=destinationCity).filter(departureDate=datetime.date(year,month,day)).filter(numSeatsRemainingEconomy__gt=0)
                trains  = list(trains )
                return render(request, 'users/trains.html',{"results":"yes", "book_type":book_type ,"some_list": trains , "class":choice})
            elif (choice == 'business'):
                trains  = Train.objects.filter(sourceLocation = sourceCity).filter(destinationLocation=destinationCity).filter(departureDate=datetime.date(year,month,day)).filter(numSeatsRemainingBusiness__gt=0)
                trains  = list(trains )
                return render(request, 'users/trains.html',{"results":"yes", "book_type":book_type ,"some_list": trains , "class":choice})
            elif(choice == 'first'):
                trains  = Train.objects.filter(sourceLocation = sourceCity).filter(destinationLocation=destinationCity).filter(departureDate=datetime.date(year,month,day)).filter(numSeatsRemainingFirst__gt=0)
                trains  = list(trains)
                return render(request, 'users/trains.html',{"results":"yes","book_type":book_type , "some_list": trains , "class":choice})
            elif(choice == 'non'):
                return render(request , 'users/trains.html' , {"results":"no"})
    return render(request , 'users/trains.html', {})



def hotel(request):
    hotel_form = HotelForm
    if(request.method == 'POST'):
        hotel_form = HotelForm(request.POST)
        if hotel_form.is_valid():
            book_type = 'Hotel'
            location = hotel_form.cleaned_data['location']
            locationArr = location.split(',')
            locationCity = locationArr[0].lower()
            startdate = hotel_form.cleaned_data['date']
            number_of_days = hotel_form.cleaned_data['number_of_days']
            choice = hotel_form.cleaned_data['hotel_type']

            print(request.POST)
            if (choice == '3'):
                hotels = Hotel.objects.filter(city = locationCity).filter(hotel_type = int(choice))
                hotels = list(hotels)
                return render(request, 'users/hotels.html',{"results":"yes", "book_type": book_type , "some_list": hotels, "class":choice, "date": startdate , "number_of_days": number_of_days})
            elif (choice == '5'):
                hotels = Hotel.objects.filter(city = locationCity).filter(hotel_type = int(choice))
                hotels = list(hotels)
                return render(request, 'users/hotels.html',{"results":"yes", "book_type": book_type , "some_list": hotels, "class":choice ,"date": startdate , "number_of_days": number_of_days})
            elif(choice == '7'):
                hotels = Hotel.objects.filter(city = locationCity).filter(hotel_type = int(choice))
                hotels = list(hotels)
                return render(request, 'users/hotels.html',{"results":"yes", "book_type": book_type , "some_list": hotels, "class":choice,"date": startdate , "number_of_days" : number_of_days})
            elif(choice == 'non'):
                return render(request , 'users/hotels.html' , {"results":"no"})



    return render(request,'users/hotels.html',{})







def payment(request , pk ):
    travel_class = request.GET.get('class')
    book_type = request.GET.get('book_type')
    if book_type == 'Flight':
        booking_details = get_object_or_404(Flight , pk = pk)
        return render(request , 'users/payment.html',{"booking_details": booking_details , "class" : travel_class , "book_type": book_type , "pk": pk})
    elif book_type == 'Train':
        booking_details = get_object_or_404(Train , pk = pk)
        return render(request , 'users/payment.html',{"booking_details": booking_details , "class" : travel_class , "book_type": book_type , "pk":pk})

    elif book_type == 'Hotel':
        nod = request.GET.get('nod')
        booking_details = get_object_or_404(Hotel , pk = pk)
        total_cost = int(booking_details.dailyCost) * int(nod)
        return render(request , 'users/payment.html',{"booking_details": booking_details , "book_type": book_type , "total_cost": total_cost , "class" : travel_class , "pk":pk})
    
    elif book_type == 'Package':
        booking_details = get_object_or_404(Destination , pk=pk)
        return render(request , 'users/payment.html',{"booking_details": booking_details, "book_type": book_type,"pk":pk ,"class" : travel_class })


def charge(request):
    if request.method == 'POST':
        print('Data:', request.POST)
        amount = float(request.POST['amount'])
        stripe_token = request.POST['stripeToken']

        obj_id = request.GET.get('id')
        obj_class = request.GET.get('class')
        obj_book_type = request.GET.get('book_type')

        print(obj_id , obj_class , obj_book_type)



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
        
        return redirect(reverse('success', kwargs={'amount': amount , 'stripe_token': stripe_token ,'obj_id':obj_id ,'obj_class':obj_class ,'obj_book_type': obj_book_type}))


def successMsg(request, amount  , obj_id , obj_class , obj_book_type, stripe_token):
    amount = amount
    user = request.user
    email_user = request.user.email
    if stripe_token != '':
        if obj_book_type == 'Flight':
            if obj_class == 'economy':
                obj = list(Flight.objects.filter(pk = obj_id).values_list('companyName','sourceLocation','destinationLocation','departureDate','departureTime','fareEconomy'))
                new_transaction = History_Flight.objects.create(user= str(user) ,brand = obj[0][0] ,source = obj[0][1] , destination = obj[0][2] , obj_date = obj[0][3] , obj_time = obj[0][4] , price = obj[0][5])
                new_transaction.save()
                html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction, 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                text_content = strip_tags(html_template)

                email = EmailMultiAlternatives(
                    "Ticket Details",
                    text_content,
                    "Travelo" +'',
                    [email_user],
                headers = {'Reply-To': 'realtorsapi@gmail.com' }

                )

                email.attach_alternative(html_template, 'text/html')
                email.send()
                print('check your mail')
            elif obj_class == 'business':
                obj = list(Flight.objects.filter(pk = obj_id).values_list('companyName','sourceLocation','destinationLocation','departureDate','departureTime','fareBusiness'))
                new_transaction = History_Flight.objects.create(user= str(user) ,brand = obj[0][0] ,source = obj[0][1] , destination = obj[0][2] , obj_date = obj[0][3] , obj_time = obj[0][4] , price = obj[0][5])
                new_transaction.save()
                html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction , 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                text_content = strip_tags(html_template)

                email = EmailMultiAlternatives(
                    "Ticket Details",
                    text_content,
                    "Travelo" +'',
                    [email_user],
                headers = {'Reply-To': 'realtorsapi@gmail.com' }

                )

                email.attach_alternative(html_template, 'text/html')
                email.send()
                print('check your mail')
            elif obj_class == 'first':
                obj = list(Flight.objects.filter(pk = obj_id).values_list('companyName','sourceLocation','destinationLocation','departureDate','departureTime','fareFirst'))
                new_transaction = History_Flight.objects.create(user= str(user) ,brand = obj[0][0] ,source = obj[0][1] , destination = obj[0][2] , obj_date = obj[0][3] , obj_time = obj[0][4] , price = obj[0][5])
                new_transaction.save()
                html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction , 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                text_content = strip_tags(html_template)

                email = EmailMultiAlternatives(
                    "Ticket Details",
                    text_content,
                    "Travelo" +'',
                    [email_user],
                headers = {'Reply-To': 'realtorsapi@gmail.com' }

                )

                email.attach_alternative(html_template, 'text/html')
                email.send()
                print('check your mail')
            else:
                return HttpResponse('Error Occured')

        elif obj_book_type == 'Train':
            obj = Train.objects.filter(pk = obj_id)
            if stripe_token != '':
                if obj_book_type == 'Train':
                    if obj_class == 'economy':
                        obj = list(Train.objects.filter(pk = obj_id).values_list('companyName','sourceLocation','destinationLocation','departureDate','departureTime','fareEconomy'))
                        print(obj)
                        new_transaction = History_Train.objects.create(user= str(user) ,brand = obj[0][0] ,source = obj[0][1] , destination = obj[0][2] , obj_date = obj[0][3] , obj_time = obj[0][4] , price = obj[0][5])
                        new_transaction.save()
                        html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction , 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                        text_content = strip_tags(html_template)

                        email = EmailMultiAlternatives(
                            "Ticket Details",
                            text_content,
                            "Travelo" +'',
                            [email_user],
                        headers = {'Reply-To': 'realtorsapi@gmail.com' }

                        )

                        email.attach_alternative(html_template, 'text/html')
                        email.send()
                        print('check your mail')
                        
                    elif obj_class == 'business':
                        obj = list(Train.objects.filter(pk = obj_id).values_list('companyName','sourceLocation','destinationLocation','departureDate','departureTime','fareBusiness'))
                        print(obj)
                        new_transaction = History_Train.objects.create(user= str(user) ,brand = obj[0][0] ,source = obj[0][1] , destination = obj[0][2] , obj_date = obj[0][3] , obj_time = obj[0][4] , price = obj[0][5])
                        new_transaction.save()
                        html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction , 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                        text_content = strip_tags(html_template)

                        email = EmailMultiAlternatives(
                            "Ticket Details",
                            text_content,
                            "Travelo" +'',
                            [email_user],
                        headers = {'Reply-To': 'realtorsapi@gmail.com' }

                        )

                        email.attach_alternative(html_template, 'text/html')
                        email.send()
                        print('check your mail')

                    elif obj_class == 'first':
                        obj = list(Train.objects.filter(pk = obj_id).values_list('companyName','sourceLocation','destinationLocation','departureDate','departureTime','fareFirst'))
                        new_transaction = History_Train.objects.create(user= str(user) ,brand = obj[0][0] ,source = obj[0][1] , destination = obj[0][2] , obj_date = obj[0][3] , obj_time = obj[0][4] , price = obj[0][5])
                        new_transaction.save()
                        html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction , 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                        text_content = strip_tags(html_template)

                        email = EmailMultiAlternatives(
                            "Ticket Details",
                            text_content,
                            "Travelo" +'',
                            [email_user],
                        headers = {'Reply-To': 'realtorsapi@gmail.com' }

                        )

                        email.attach_alternative(html_template, 'text/html')
                        email.send()
                        print('check your mail')
                    else:
                        return HttpResponse('Error Occured')
        
        elif obj_book_type == 'Package':
            obj = Destination.objects.filter(pk = obj_id)
            if stripe_token != '':
                obj = list(Destination.objects.filter(pk = obj_id).values_list('destination_name','package_price'))
                new_transaction = History_Package.objects.create(user= str(user) ,name = obj[0][0] ,price = obj[0][1])
                new_transaction.save()
                html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction , 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                text_content = strip_tags(html_template)

                email = EmailMultiAlternatives(
                    "Ticket Details",
                    text_content,
                    "Travelo" +'',
                    [email_user],
                headers = {'Reply-To': 'realtorsapi@gmail.com' }

                )

                email.attach_alternative(html_template, 'text/html')
                email.send()
                print('check your mail')
            else:
                return HttpResponse('Error Occured')

                
        
        elif obj_book_type == 'Hotel':
            obj = Hotel.objects.filter(pk = obj_id)
            if stripe_token != '':
                if obj_book_type == 'Hotel':
                    if obj_class == '3':
                        obj = list(Hotel.objects.filter(pk = obj_id).values_list('hotelName','hotel_type','hotel_image','address','city'))
                        new_transaction = History_Hotel.objects.create(user= str(user) ,name = obj[0][0] ,type = obj[0][1] , image = obj[0][2] , price = amount , address = obj[0][3] , city = obj[0][4])
                        new_transaction.save()
                        html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction , 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                        text_content = strip_tags(html_template)

                        email = EmailMultiAlternatives(
                            "Ticket Details",
                            text_content,
                            "Travelo" +'',
                            [email_user],
                        headers = {'Reply-To': 'realtorsapi@gmail.com' }

                        )

                        email.attach_alternative(html_template, 'text/html')
                        email.send()
                        print('check your mail')
                    elif obj_class == '5':
                        obj = list(Hotel.objects.filter(pk = obj_id).values_list('hotelName','hotel_type','hotel_image','address','city'))
                        new_transaction = History_Hotel.objects.create(user= str(user) ,name = obj[0][0] ,type = obj[0][1] , image = obj[0][2] , price = amount , address = obj[0][3] , city = obj[0][4])
                        new_transaction.save()
                        html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction , 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                        text_content = strip_tags(html_template)

                        email = EmailMultiAlternatives(
                            "Ticket Details",
                            text_content,
                            "Travelo" +'',
                            [email_user],
                        headers = {'Reply-To': 'realtorsapi@gmail.com' }

                        )

                        email.attach_alternative(html_template, 'text/html')
                        email.send()
                        print('check your mail')
                    elif obj_class == '7':
                        obj = list(Hotel.objects.filter(pk = obj_id).values_list('hotelName','hotel_type','hotel_image','address','city'))
                        new_transaction = History_Hotel.objects.create(user= str(user) ,name = obj[0][0] ,type = obj[0][1] , image = obj[0][2] , price = amount , address = obj[0][3] , city = obj[0][4])
                        new_transaction.save()
                        html_template = render_to_string("users/ticket_template.html",{'new_transaction': new_transaction , 'obj_class':obj_class , 'obj_book_type': obj_book_type})
                        text_content = strip_tags(html_template)

                        email = EmailMultiAlternatives(
                            "Ticket Details",
                            text_content,
                            "Travelo" +'',
                            [email_user],
                        headers = {'Reply-To': 'realtorsapi@gmail.com' }

                        )

                        email.attach_alternative(html_template, 'text/html')
                        email.send()
                        print('check your mail')
                    else:
                        return HttpResponse('Error Occured')






    return render(request, 'users/success.html', {'amount':amount , 'token': stripe_token })





def search(request):
    if request.method == "GET":
        searchfield = request.GET.get("search")
        obj = []
        cat = request.GET.get("category")
        lenght = 0

        if cat == "hotels":
            obj = Hotel.objects.filter(hotelName__icontains=searchfield)
            lenght = obj.count()
        elif cat == "package":
            obj = Destination.objects.filter(destination_name__icontains=searchfield)
            lenght = obj.count()
        


    # obj = Hotel.objects.filter(hotelName__icontains="f")

    # print(obj.all())
    
    return render(request, 'users/search.html', {"obj":obj, "cat": cat, "length": lenght})

