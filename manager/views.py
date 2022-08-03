import json

from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers import serialize
from django.db.models import Sum, Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView

from manager.forms import UserRegisterForm, DonationAddForm
from users.forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm, CustomUserEditForm, \
    CustomPasswordChangeForm
from users.models import User
from .models import Donation, Institution, Category
from django.db.models import F


from django.shortcuts import resolve_url


class LandingPage(View):
    def pagination(self, institution_type):
        paginator = Paginator(Institution.objects.filter(type=institution_type), 5)
        page = self.request.GET.get('page')

        try:
            insitutions_by_type = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            insitutions_by_type = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            insitutions_by_type = paginator.page(paginator.num_pages)

        return insitutions_by_type

    def get(self, request):
        insitutions = Institution.objects.all()

        total_donated_quantity = Donation.objects.all().aggregate(Sum('quantity'))
        donated_institutions = insitutions.filter(donation__quantity__gt=0).distinct().count()

        foundations = self.pagination(institution_type=1)
        ngos = self.pagination(institution_type=2)
        charity_collections = self.pagination(institution_type=3)

        context = {
            'total_donated_quantity': total_donated_quantity,
            'donated_institutions': donated_institutions,
            'foundations': foundations,
            'ngos': ngos,
            'charity_collections': charity_collections
        }
        return render(request, 'mytemplates/index.html', context)


class AddDonation(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'mytemplates/form.html', {'categories': categories})

    def post(self, request):
        form = DonationAddForm(request.POST)

        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()

            categories = form.cleaned_data.get('categories')
            donation.categories.set(categories)
            donation.save()
            return redirect('donation-confirmation')

        return redirect('add-donation')


class GetInstitutionApiView(View):
    def get(self, request):
        category_ids = request.GET.getlist('id')

        institutions = Institution.objects.all()
        for category_id in category_ids:
            institutions = institutions.filter(categories__id=category_id)

        data = serialize('json', institutions)
        return HttpResponse(data, content_type="application/json")


class ConfirmationView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        return render(request, 'mytemplates/form_confirmation.html')


class Login(LoginView):
    template_name = 'mytemplates/login.html'
    form_class = CustomAuthenticationForm


class Register(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_authenticated

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


class UserDetailsView(ListView):
    model = Donation
    template_name = 'mytemplates/user_details.html'

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user)


class GetDonationApiView(View):
    def get(self, request):
        donation = get_object_or_404(Donation, id=request.GET.get('id'))

        if not donation.is_taken:
            donation.is_taken = True
        else:
            donation.is_taken = False
        donation.save()

        donations = Donation.objects.filter(user=self.request.user)

        data = serialize('json', donations, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")


class UserEditView(UpdateView):
    model = User
    success_url = reverse_lazy('landing-page')

    form_class = CustomUserEditForm
    template_name = 'mytemplates/user_edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """View allows users to change their passwords"""
    form_class = CustomPasswordChangeForm
    login_url = reverse_lazy('landing-page')
    template_name = 'mytemplates/user_password_change.html'

    def get_success_url(self):
        """Method forces loggin-out users accaouts and redirects to log-in View"""
        logout(self.request)
        return reverse_lazy('login-page')












































































































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