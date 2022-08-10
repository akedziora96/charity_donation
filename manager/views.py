from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers import serialize
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from manager.forms import DonationAddForm, LoggedUserMailContactForm, AnnonymousMailContactForm
from users.models import User
from .models import Donation, Institution, Category
from django.core.mail import send_mail
from django.conf import settings

PAGINATION_OBJECTS_PER_PAGE = 1


class LandingPage(View):
    def first_page(self, institution_type):
        paginator = Paginator(Institution.objects.filter(type=institution_type), PAGINATION_OBJECTS_PER_PAGE)
        return paginator.page(1)

    def get(self, request):
        insitutions = Institution.objects.all()

        total_donated_quantity = Donation.objects.all().aggregate(Sum('quantity'))
        donated_institutions = insitutions.filter(donation__quantity__gt=0).distinct().count()

        get_type_num_by_type_name = {value: key for key, value in Institution.TYPES}
        foundations = self.first_page(institution_type=get_type_num_by_type_name.get('Fundacja'))
        ngos = self.first_page(institution_type=get_type_num_by_type_name.get('Organizacja Pozarządowa'))
        charity_collections = self.first_page(institution_type=get_type_num_by_type_name.get('Zbiórka Lokalna'))

        context = {
            'total_donated_quantity': total_donated_quantity,
            'donated_institutions': donated_institutions,
            'foundations': foundations,
            'ngos': ngos,
            'charity_collections': charity_collections
        }
        return render(request, 'manager/index.html', context)


class DonationAddView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'manager/form.html', {'categories': categories})


class SendContactMailView(View):
    def send_mail_to_user(self, first_name, last_name, email):
        subject = 'Potwierdzenie otrzymania wiadomości'
        email_body = f'{first_name} {last_name}, dziękujemy za kontakt. ' \
                     f'Administrator odezwie się do Ciebie najszybciej jak to możliwe'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, email_body, email_from, recipient_list)

    def send_mail_to_admins(self, first_name, last_name, email, user_message):
        subject = f'Wiadomość od {first_name} {last_name} ({email})'
        email_body = f'Użytkownik o mailu {email} wysłał następującą wiadmość: "{user_message}".'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in User.objects.filter(is_superuser=True)]
        send_mail(subject, email_body, email_from, recipient_list)

    def get(self, request):
        url = reverse('landing-page') + '#contact'
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

            return render(request, 'manager/form_contact_confirmation.html', {'name': first_name})

        return render(request, 'manager/form_contact_failure.html')


class ConfirmationView(View):
    def get(self, request):
        return render(request, 'manager/form_confirmation.html')


# API VIEWS


class PaginationApiView(View):
    def get(self, request):
        page = request.GET.get('page')
        institution_type = request.GET.get('type')
        paginator = Paginator(Institution.objects.filter(type=institution_type), PAGINATION_OBJECTS_PER_PAGE)

        try:
            institutions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            institutions = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            institutions = paginator.page(paginator.num_pages)

        data = serialize('json', institutions, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type="application/json")


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


class GetInstitutionApiView(View):
    def get(self, request):
        category_ids = request.GET.getlist('id')

        institutions = Institution.objects.all()
        for category_id in category_ids:
            institutions = institutions.filter(categories__id=category_id)

        data = serialize('json', institutions)
        return HttpResponse(data, content_type="application/json")


class SaveDonationApiView(View):
    def send_confirmation_mail(self, user, donation):
        subject = 'Potwierdzenie otrzymania darowizny'
        email_body = f'{user.first_name} {user.last_name}, dziękujemy za przekazanie darowizny. ' \
                     f'Podsumowanie:\nOrganizacja obdarowana:{donation.institution}\nRzeczy przekazane:\n' \
                     f'{donation.quantity} worków: {donation.categories}\nMiejsce odbioru: {donation.address}\n' \
                     f'Miasto: {donation.city}\nKod pocztowy: {donation.zip_code}\nNr Twojego telefonu: ' \
                     f'{donation.phone_number}\nData odbioru: {donation.pick_up_date}\nGodzina odbioru: ' \
                     f'{donation.pick_up_time}\nKomentarz do odbioru: {donation.pick_up_comment}\n\n' \
                     f'Pozdrawiamy,\nAdministracja strony'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, email_body, email_from, recipient_list)

    def post(self, request):
        form = DonationAddForm(request.POST)

        if form.is_valid():
            user = request.user

            donation = form.save(commit=False)
            donation.user = user
            donation.save()

            categories = form.cleaned_data.get('categories')
            donation.categories.set(categories)
            donation.save()

            self.send_confirmation_mail(user=user, donation=donation)

            # data = serialize('json', Donation.objects.filter(id=donation.id), use_natural_foreign_keys=True)
            # return HttpResponse(data, content_type="application/json")
            return JsonResponse({'status': 'success', 'url': reverse('confirm-donation')})

        return JsonResponse({'status': 'error'})