from django import template
from schoolapp.models import Notice

register = template.Library()


@register.simple_tag
def get_notices():
    return Notice.objects.filter(is_active=True)[:5]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def range_filter(value):
    return range(value)
