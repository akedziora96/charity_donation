"""manager URL Configuration

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
from django.urls import path
from manager import views

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing-page'),

    path('add-donation/', views.AddDonation.as_view(), name='add-donation'),
    path('contact-us/', views.SendContactMailView.as_view(), name='contact'),

    # API's views
    path('get-institution-api/', views.GetInstitutionApiView.as_view(), name='institution-api'),
    path('get-donation-api/', views.GetDonationApiView.as_view(), name='donation-api'),
    path('get-page-api/', views.PaginationApiView.as_view(), name='pagination-api'),
]
