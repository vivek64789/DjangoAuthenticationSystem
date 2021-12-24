from os import name
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.loginUser, name= "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerUser, name="register"),
    path('validate-username/', views.registerUsernameValidation, name="validate-username"),
    path('confirm-password/', views.registerConfirmPassword, name="confirm-password"),
    path('validate-email/', views.registerEmailValidation, name="validate-email"),
    path('activate-user/', views.activateUser, name="activateUser"),
    path('activate/', views.activateUserLogin, name="activate"),
    path('welcome', views.welcomeUser, name="welcomeuser")
]
