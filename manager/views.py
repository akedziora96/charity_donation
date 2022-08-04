from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers import serialize
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from manager.forms import DonationAddForm, LoggedUserMailContactForm, AnnonymousMailContactForm
from users.models import User
from .models import Donation, Institution, Category
from django.core.mail import send_mail
from django.conf import settings


class LandingPage(View):
    def pagination(self, institution_type):
        paginator = Paginator(Institution.objects.filter(type=institution_type), 1)
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
        return render(request, 'manager/index.html', context)


class AddDonation(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'manager/form.html', {'categories': categories})

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
        return render(request, 'manager/form_confirmation.html')


class UserDonationsView(ListView):
    model = Donation
    template_name = 'manager/user_details.html'

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


class SendContactMailView(View):
    def send_mail_to_user(self, first_name, last_name, email):
        subject = 'Potwierdzenie otrzymania wiadomości'
        email_body = f'{first_name} {last_name}, dziękujemy za kontakt. ' \
                     f'Administrator odezwie się do Ciebie najszybciej jak to możliwe'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [f'{email}']
        send_mail(subject, email_body, email_from, recipient_list)

    def send_mail_to_admins(self, first_name, last_name, email, user_message):
        subject = f'Wiadomość od {first_name} {last_name} ({email})'
        email_body = f'Użytkownik o mailu {email} wysłał następującą wiadmość: "{user_message}".'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in User.objects.filter(is_superuser=True)]
        send_mail(subject, email_body, email_from, recipient_list)

    def get(self, request):
        url = reverse_lazy('landing-page') + '#contact'
        return redirect(url)

    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            form = AnnonymousMailContactForm(request.POST)
        else:
            form = LoggedUserMailContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if not user.is_authenticated:
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                email = data.get('email')
            else:
                first_name = user.first_name
                last_name = user.last_name
                email = user.email

            user_message = data.get('message')

            self.send_mail_to_user(
                first_name=first_name, last_name=last_name, email=email
            )
            self.send_mail_to_admins(
                first_name=first_name, last_name=last_name, email=email, user_message=user_message
            )

            return render(request, 'manager/contact_confirmation.html', {'name': first_name})































































































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