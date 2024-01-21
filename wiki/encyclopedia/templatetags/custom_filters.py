# custom_filters.py
from django import template
from django.template.defaultfilters import stringfilter
import markdown2

register = template.Library()

@register.filter(name='markdownify')
@stringfilter
def markdownify(value):
    return markdown2.markdown(value)