"""charity_donation_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LandingPage.as_view(), name='landing-page'),
    path('add_donation/', views.AddDonation.as_view(), name='add-donation'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),

    # path('form/', views.form),
    # path('form_confirmation/', views.form_confirmation),
    # path('form_login/', views.login),
    # path('form_register/', views.register),
    # path('base/', views.base),
    # path('index2/', views.index2),
    # path('form2/', views.form2),
    # path('form_confirmation2/', views.form_confirmation2),
    # path('form_login2/', views.login2),
    # path('form_register2/', views.register2),
]
