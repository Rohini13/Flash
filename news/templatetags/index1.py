from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def index2(indexable, i):
    return indexable[2*i]