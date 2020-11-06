from django import template
register = template.Library()
import json

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def get_item(json, part):
    return json.part

#https://stackoverflow.com/questions/4651172/reference-list-item-by-index-within-django-template