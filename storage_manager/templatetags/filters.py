from django import template
from storage_manager.models import Item

register = template.Library()


@register.filter(name='item_count')
def item_count(value):
    return Item.objects.filter(storage=value).count()


@register.filter(name='item_quantity')
def item_quantity(value):
    result = 0
    for i in Item.objects.filter(storage=value):
        result += i.quantity

    return result
