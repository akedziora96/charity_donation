from django import template

from manager.forms import AnnonymousMailContactForm, LoggedUserMailContactForm

register = template.Library()


@register.simple_tag
def annonymous_contact_form():
    return AnnonymousMailContactForm()


@register.simple_tag
def logged_user_contact_form():
    return LoggedUserMailContactForm()