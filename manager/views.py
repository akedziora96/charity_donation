from django.db.models import Sum, Count
from django.shortcuts import render
from django.views import View

from .models import Donation, Institution
from django.db.models import F


class LandingPage(View):
    def get(self, request):
        total_donated_quantity = Donation.objects.all().aggregate(Sum('quantity'))
        insitutions = Institution.objects.all()
        donated_institutions = insitutions.filter(donation__quantity__gt=0).distinct().count()
        context = {
            'total_donated_quantity': total_donated_quantity,
            'institutions': insitutions,
            'donated_institutions': donated_institutions
        }
        return render(request, 'mytemplates/index.html', context)


class AddDonation(View):
    def get(self, request):
        return render(request, 'mytemplates/form.html')


class Login(View):
    def get(self, request):
        return render(request, 'mytemplates/login.html')


class Register(View):
    def get(self, request):
        return render(request, 'mytemplates/register.html')























































































































# def index(request):
#     return render(request, 'defaults/index.html')
#
#
# def form_confirmation(request):
#     return render(request, 'defaults/form-confirmation.html')
#
#
# def form(request):
#     return render(request, 'defaults/form.html')
#
#
# def login(request):
#     return render(request, 'defaults/login.html')
#
#
# def register(request):
#     return render(request, 'defaults/register.html')
#
#
# def base(request):
#     return render(request, 'base.html')
#
#
# def index2(request):
#     return render(request, 'mytemplates/index.html')
#
#
# def form2(request):
#     return render(request, 'mytemplates/form.html')
#
#
# def form_confirmation2(request):
#     return render(request, 'mytemplates/form_confirmation.html')
#
#
# def login2(request):
#     return render(request, 'mytemplates/login.html')
#
#
# def register2(request):
#     return render(request, 'mytemplates/register.html')