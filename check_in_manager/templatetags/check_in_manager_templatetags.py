from django import template
from check_in_manager.models import Offer

register = template.Library()


@register.filter(name='check_if_order_has_offers')
def item_count(order_id):
    offers = Offer.objects.filter(offer_order_id=order_id).count()
    if offers:
        return True
    return False


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})
