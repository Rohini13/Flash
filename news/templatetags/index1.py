from django import template
register = template.Library()


@register.filter
def get_value(indexable, i):
    return indexable[i]


@register.filter
def check(indexable, i):
    if (len(indexable) > i):
        return True
    else:
        return False


@register.filter
def index(indexable, i):
    if (len(indexable) > i):
        return indexable[i]['image']
    else:
        return None


@register.filter
def index1(indexable, i):
    if (len(indexable) > i):
        return indexable[i]['title']
    else:
        return None


@register.filter
def index2(indexable, i):
    if(len(indexable)>i):
        return indexable[i]['source']
    else:
        return None


@register.filter
def logo(indexable, i):
    if(len(indexable)>i):
        return indexable[i]['logo']
    else:
        return None

