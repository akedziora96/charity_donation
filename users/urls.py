"""Users URL Configuration

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
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.Login.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout-page'),

    path('register/', views.Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>', views.UserActivateView.as_view(), name='activate'),

    path('details/', views.UserDetailView.as_view(), name='user-details'),

    path('edit/', views.UserEditView.as_view(), name='user-edit'),
    path('password/change/', views.UserPasswordChangeView.as_view(), name='user-change-change-password'),

    path('password/reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'password/reset/<uidb64>/<token>/',
        views.UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
