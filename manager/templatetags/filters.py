from django import template

register = template.Library()


@register.filter
def get_categories_names(institution):
    return ", ".join(institution.categories.values_list('name', flat=True))


@register.filter
def get_by_type(qs, institution_type):
    return qs.filter(type=institution_type)
