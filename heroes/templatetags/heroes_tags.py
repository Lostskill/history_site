from django import template
from heroes.models import *

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('heroes\index.html')
def show_categories(sort=None, rub_selected=0):
    if not sort:
        rubs = Category.objects.all()
    else:
        rubs = Category.objects.order_by(sort)

    return {"rubs": rubs, "rub_selected": rub_selected}
