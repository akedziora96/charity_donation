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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin-page'),
    path('', views.LandingPage.as_view(), name='landing-page'),

    path('add_donation/', views.AddDonation.as_view(), name='add-donation'),
    path('add_donation/confirmation/', views.ConfirmationView.as_view(), name='donation-confirmation'),
    path('get_institution_api/', views.GetInstitutionApiView.as_view(), name='institution-api'),
    path('user_details/', views.UserDetailsView.as_view(), name='user-details'),
    path('get_donation_api/', views.GetDonationApiView.as_view(), name='donation-api'),
    path('user_edit/', views.UserEditView.as_view(), name='user-edit'),
    path('user_change_password/', views.UserPasswordChangeView.as_view(), name='user-change-change-password'),
    path('activate/<uidb64>/<token>', views.UserActivateView.as_view(), name='activate'),

    path('login/', views.Login.as_view(redirect_authenticated_user=True), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout-page'),

    path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('contact_us/', views.SendContactMailView.as_view(), name='contact'),



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
