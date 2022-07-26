from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, ListView

from manager.models import Donation
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, CustomUserEditForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm
)
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
from .utils import account_activation_token
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib import messages


class Login(LoginView):
    form_class = CustomAuthenticationForm


class UserRegisterView(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('landing-page')

    def send_activation_token(self, user):
        """Generates and sends a token which enables user to activate himself/herself."""
        user = user
        domain = get_current_site(self.request).domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        link = reverse('activate', kwargs={'uidb64': uid, 'token': token})

        activate_url = 'http://' + domain + link

        subject = 'Dziękujemy za rejestrację'
        email_body = f'W celu aktywacji konta prosimy o klinięcie poniższego linku:\n {activate_url}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, email_body, email_from, recipient_list)

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        """Creates a new inactive user."""
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()

            self.send_activation_token(user=user)

            messages.success(
                request, 'Konto zostało pomyślnie utworzone. Na maila wysłaliśmy link z kodem aktywacyjnym.'
            )
            return redirect('login')

        return render(request, 'users/register.html', {'form': form})


class UserActivateView(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('landing-page')

    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if account_activation_token.check_token(user, token) and not user.is_active:
                user.is_active = True
                user.save()
                status = 'user is now activated'
            else:
                status = 'user is already activated'

        except ObjectDoesNotExist or DjangoUnicodeDecodeError:
            status = 'decoding error'

        return render(request, 'users/activation_confirm.html', {'status': status})


class UserDetailView(LoginRequiredMixin, ListView):
    """
    Displays user's details and history of user's donatiotions (see also GetDonationApiView in manager's views).
    """
    model = Donation
    login_url = reverse_lazy('login')
    template_name = 'users/user_details.html'

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user)


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('landing-page')

    form_class = CustomUserEditForm
    template_name = 'users/user_edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    login_url = reverse_lazy('landing-page')

    def get_success_url(self):
        """Logouts a logged-in user and redirects to UserPasswordChangeDoneView View."""
        logout(self.request)
        return reverse_lazy('password_change_done')


class UserPasswordChangeDoneView(View):
    """Subtitutes generic PasswordChangeDoneView, allowing acess for not logged-in users."""
    def get(self, request):
        return render(request, 'registration/password_change_done.html')


class UserPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm


