from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import OrderForm, OfferForm, InclusionForm, SpecOccasionForm, SourceForm, OfferFormSet
from .models import *
from .choices import ORDER_STATUS_CHOICES




def index(request):
    if request.user.is_superuser:
        orders = reversed(Order.objects.all())
        orders_ids = [order.id for order in Order.objects.all()]
    else:
        orders = reversed(Order.objects.filter(order_creator=request.user.id))
        orders_ids = [order.id for order in Order.objects.filter(
            order_creator=request.user.id)]

    offers = Offer.objects.filter(
        offer_order_id__in=[order_id for order_id in orders_ids])
    ctx = {
        'orders': orders,
        'offers': offers
    }
    if request.method == 'POST':
        if request.POST.get('from_date') and request.POST.get('to_date'):
            orders = Order.objects.filter(
                order_guest_check_in_date__range=(request.POST.get('from_date'), request.POST.get('to_date')))
            ctx['orders'] = orders
    return render(request, "check_in_manager/index.html", ctx)


def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    ctx = {
        'order': order,
    }
    return render(request, 'check_in_manager/order_details.html', ctx)


def edit_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderForm(instance=order, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(order_id))
    else:
        form = OrderForm(instance=order)

    ctx = {
        'order': order,
        'form': form
    }
    return render(request, 'check_in_manager/edit_order.html', ctx)


def create_order(request):
    source = Source.objects.all()
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.order_creator = request.user
            new_order.save()
            return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(new_order.id))
    else:
        form = OrderForm()
    ctx = {
        'form': form
    }
    return render(request, 'check_in_manager/create_order.html', ctx)


def create_offers(request, order_id):
    if request.method == 'POST':
        formset = OfferFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                instance = form.save(commit=False)
                if instance.offer_price_per_night and instance.offer_tax:
                    instance.offer_order_id = order_id
                    form.save()
            return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(order_id))
    else:
        formset = OfferFormSet()
    ctx = {
        'formset': formset
    }
    return render(request, 'check_in_manager/create_offers.html', ctx)


def send_offers(request, order_id):
    order_status_list = dict((key, val) for key, val in ORDER_STATUS_CHOICES)
    offers = Offer.objects.filter(offer_order_id=order_id)
    Order.objects.filter(id=order_id).update(
        order_status=order_status_list['waiting_for_client_to_accept_offer']
    )
    for offer in offers:
        print(offer)
    return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(order_id))
