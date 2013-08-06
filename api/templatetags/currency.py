from django import template

register = template.Library()

@register.filter
def cents_to_dollars(value):
    return '{0:.2f}'.format(value / 100.0)