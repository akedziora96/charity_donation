import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.serializers import serialize
from django.db.models import Sum, Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from manager.forms import UserRegisterForm
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from users.models import User
from .models import Donation, Institution, Category
from django.db.models import F


from django.shortcuts import resolve_url


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


class AddDonation(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        categories = Category.objects.all()
        insitutions = None
        print(insitutions)
        return render(request, 'mytemplates/form.html', {'categories': categories, 'insitutions': insitutions})

    def post(self, request):
        print(request.POST.getlist('categories'))
        print(request.POST.get('bags'))
        print(request.POST.get('organization'))
        return redirect('landing-page')


class GetInstitutionApiView(View):
    def get(self, request):
        category_ids = request.GET.getlist('id')

        institutions = Institution.objects.all()
        for category_id in category_ids:
            institutions = institutions.filter(categories__id=category_id)

        data = serialize('json', institutions)
        return HttpResponse(data, content_type="application/json")


class Login(LoginView):
    template_name = 'mytemplates/login.html'
    form_class = CustomAuthenticationForm


class Register(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'mytemplates/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            return redirect('login')

        return render(request, 'mytemplates/register.html', {'form': form})






















































































































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