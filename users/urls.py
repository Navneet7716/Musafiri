from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserPasswordResetForm

urlpatterns = [



    path("login/", views.login, name="login"),
    path("register/",views.register,name="register"),
    path("",views.home,name="home"),
    path("flight/",views.flight,name="flight"),
    path("train/" ,views.train,name="train"),
    path("hotel/",views.hotel , name="hotel"),
    path('logout/',views.logoutUser,name="logout"),
    path('contact/',views.contact , name="contact"),
    path('about/',views.about,name="about"),
    path('blog/',views.blog,name="blog"),
    path('destination_details/<int:pk>',views.destination_details,name="destination_details"),
    path('single-blog/',views.single_blog,name="single_blog"),
    path('travel_destination/',views.travel_destination,name="travel_destination"),
    path('payment/<int:pk>',views.payment,name="payment"),
    path('graphs/',views.graph , name="graph"),
    path('charge/', views.charge, name="charge"),
    path('success/<str:amount>/<str:obj_id>/<str:obj_class>/<str:obj_book_type>/<str:stripe_token>/', views.successMsg, name="success"),
    path('history/',views.history , name="history"),
    path('search/', views.search, name="search"),



    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="users/password_reset.html",  form_class=UserPasswordResetForm),
    name="reset_password"),
    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"),
    name="password_reset_done"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_form.html"),
    name="password_reset_confirm"),
    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
    name="password_reset_complete")
]
