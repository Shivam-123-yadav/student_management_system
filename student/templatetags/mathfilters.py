# student/templatetags/mathfilters.py
from django import template

register = template.Library()

@register.filter(name='sub')
def sub(value, arg):
    """Subtract arg from value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0