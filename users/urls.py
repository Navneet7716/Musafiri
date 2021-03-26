from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [



    path("login/", views.login, name="login"),
    path("register/",views.register,name="register"),
    path("home/",views.home,name="home"),
    path('logout/',views.logoutUser,name="logout"),
    path('contact/',views.contact , name="contact"),
    path('about/',views.about,name="about"),
    path('blog/',views.blog,name="blog"),
    path('destination_details/',views.destination_details,name="destination_details"),
    path('single-blog/',views.single_blog,name="single_blog"),
    path('travel_destination/',views.travel_destination,name="travel_destination"),







    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
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
