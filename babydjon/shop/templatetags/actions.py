from django import template
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
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

@register.simple_tag
def delAttr(val, attr):
    if attr in val:
        del val[attr]
    return ""