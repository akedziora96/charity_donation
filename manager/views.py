from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers import serialize
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from manager.forms import DonationAddForm, LoggedUserMailContactForm, AnnonymousMailContactForm
from users.models import User
from .models import Donation, Institution, Category
from django.core.mail import send_mail
from django.conf import settings

from .templatetags.filters import get_categories_names

PAGINATION_OBJECTS_PER_PAGE = 5


class LandingPageView(View):
    """
    Displays total donatedet bags and number of institutions which recieved donations. Also, it displays
    first page of every type paginated institutions. The rest of pages are dinamicaly loaded, without page reload,
    with the use of JavaScript script, which fetches pages from PaginationApiView.
    """
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
    """
    Renders form which enables potential donors to express willingness to donate one of selected institutions and fill
    key information about it (see Donation model). Categories are passed to context because they are on a first step of
    the form. Rest of form is supported by JS to provide dynamic switch steps of itself.
    """
    login_url = reverse_lazy('login')

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'manager/form.html', {'categories': categories})


class DonationConfirmationView(LoginRequiredMixin, View):
    """Renders confirmation information about sucess donation."""
    login_url = reverse_lazy('login')

    def get(self, request):
        return render(request, 'manager/form_confirmation.html')


class ContactConfirmationView(View):
    """Renders confirmation information about sucess donation."""
    def get(self, request):
        return render(request, 'manager/form_contact_confirmation.html')


# API VIEWS


class PaginationApiView(View):
    """
    Provides acess to Page object basing on number of page and type of institution.
    It is used to provide pagination without page reloading.
    """
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


class GetDonationApiView(LoginRequiredMixin, View):
    """
    Provides acess to loged-in user's all Donation objects.
    Also, enables to mark which donation was taken by institution without page reloading.
    """
    login_url = reverse_lazy('login')

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


class GetInstitutionApiView(LoginRequiredMixin, View):
    """
    Provides acess to Institution object which simultaneously accepts the gifts of all categories selected by the user,
    which were marked by her/him on first step of form. When user marks no checkbox, it returns all institutions in db.
    """
    login_url = reverse_lazy('login')

    def get(self, request):
        category_ids = request.GET.getlist('id')

        institutions = Institution.objects.all()
        for category_id in category_ids:
            institutions = institutions.filter(categories__id=category_id)

        data = serialize('json', institutions)
        return HttpResponse(data, content_type='application/json')


class SaveDonationApiView(LoginRequiredMixin, View):
    """Creates Donation institution and send confirmation mail to the donor."""
    login_url = reverse_lazy('login')

    def send_confirmation_mail(self, user, donation):
        subject = 'Potwierdzenie otrzymania darowizny'
        email_body = f'{user.first_name} {user.last_name}, dziękujemy za przekazanie darowizny.\n\n'\
                     f'Podsumowanie:\n'\
                     f'Organizacja obdarowana: {donation.institution}\n'\
                     f'Przekazano {donation.quantity} worków: {get_categories_names(donation)}\n'\
                     f'Miejsce odbioru: {donation.address}\n'\
                     f'Miasto: {donation.city}\n'\
                     f'Kod pocztowy: {donation.zip_code}\n'\
                     f'Nr Twojego telefonu: {donation.phone_number}\n'\
                     f'Data odbioru: {donation.pick_up_date}\n'\
                     f'Godzina odbioru: {donation.pick_up_time}\n'\
                     f'Komentarz do odbioru: {donation.pick_up_comment}\n\n'\
                     f'Pozdrawiamy,\n'\
                     f'Administracja strony'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, email_body, email_from, recipient_list)

    def post(self, request):
        user = request.user
        form = DonationAddForm(request.POST, user=user)

        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = user
            donation.save()

            categories = form.cleaned_data.get('categories')
            donation.categories.set(categories)
            donation.save()

            self.send_confirmation_mail(user=user, donation=donation)

            return JsonResponse({'status': 'success', 'url': reverse('confirm-donation')})

        errors_messages = {field: errors for field, errors in form.errors.items()}

        is_double_sent = form.has_error('__all__', 'double_sent')
        is_date_from_past = form.has_error('__all__', 'date_from_past')
        is_hour_from_past = form.has_error('__all__', 'hour_from_past')

        if is_double_sent or is_date_from_past or is_hour_from_past:
            error_message_to_json = errors_messages.get('__all__')
        else:
            error_message_to_json = 'Błąd walidacji formularza.<br>Wykonaj reset (CTRL+F5) przeglądarki.'

        return JsonResponse({'status': 'error', 'error_message': error_message_to_json})


class SendContactMailApiView(View):
    """
    Provides users to send mail to admins from every page of this app, through contact form placed in a footer.
    """
    def send_mail_to_user(self, first_name, last_name, email):
        subject = 'Potwierdzenie otrzymania wiadomości'
        email_body = f'{first_name} {last_name}, dziękujemy za kontakt.\n '\
                     f'Administrator odezwie się do Ciebie najszybciej jak to możliwe.'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, email_body, email_from, recipient_list)

    def send_mail_to_admins(self, first_name, last_name, email, user_message):
        subject = f'Wiadomość od {first_name} {last_name} ({email})'
        email_body = f'Użytkownik o mailu {email} wysłał następującą wiadmość: "{user_message}"'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in User.objects.filter(is_superuser=True)]
        send_mail(subject, email_body, email_from, recipient_list)

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

            return JsonResponse({'status': 'success', 'url': reverse('confirm-contact')})
        fields_errors = {field: ','.join(errors) for field, errors in form.errors.items()}
        return JsonResponse({'status': 'error', 'fields_errors': fields_errors})