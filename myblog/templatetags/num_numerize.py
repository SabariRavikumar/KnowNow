from numerize import numerize
from django import template


register = template.Library()

@register.simple_tag()
def round_number(value):
    a = numerize.numerize(value)
    return a
    
@register.simple_tag()
def range(min=5):
    return range(min)


