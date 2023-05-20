from django import template
register = template.Library()

@register.simple_tag
def inc(val):
    return val + 1

@register.simple_tag
def zero():
    return 0

@register.simple_tag
def setVal(val):
    return val

@register.simple_tag
def delSpace(s):
    return s.replace(" ", "")