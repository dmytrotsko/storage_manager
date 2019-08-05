from django import template
from storage_manager.models import Item

register = template.Library()


@register.filter(name='item_count')
def item_count(value):
    return Item.objects.filter(storage=value).count()
