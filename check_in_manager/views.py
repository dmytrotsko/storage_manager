from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import (OrderForm,
                    OfferForm,
                    InclusionForm,
                    SpecOccasionForm,
                    SourceForm,
                    OfferFormSet,
                    AcceptOfferForm,
                    DeclineOfferForm
                    )
from .models import *
from messaging.utils import send_email_message


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
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        formset = OfferFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                instance = form.save(commit=False)
                if instance.offer_price_per_night and instance.offer_tax:
                    instance.offer_order_id = order_id
                    form.save()
            order.order_status = 1
            order.save()
            return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(order_id))
    else:
        formset = OfferFormSet()
    ctx = {
        'formset': formset
    }
    return render(request, 'check_in_manager/create_offers.html', ctx)


def send_offers(request, order_id):
    offers = Offer.objects.filter(offer_order_id=order_id)
    order = Order.objects.get(id=order_id)
    try:
        send_email_message(
            template_name='send_offers',
            recipients=['dmytrotsko@gmail.com'],
            sender="dmytrotsko@gmail.com",
            context={
                'offers': offers
            },
        )
        order.order_status = 2
        order.save()
    except Exception as e:
        order.order_offers_sent = False
    order.save()
    return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(order_id))


def accept_offer(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = AcceptOfferForm(instance=order, data=request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_creator = request.user
            order.order_status = 3
            order.save()
            return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(order.id))
    else:
        form = AcceptOfferForm(instance=order)
    ctx = {
        'order': order,
        'form': form
    }
    return render(request, 'check_in_manager/accept_offer.html', ctx)


def decline_offer(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = DeclineOfferForm(instance=order, data=request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_creator = request.user
            order.order_status = 4
            order.save()
            return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(order.id))
    else:
        form = DeclineOfferForm(instance=order)
    ctx = {
        'order': order,
        'form': form
    }
    return render(request, 'check_in_manager/decline_offer.html', ctx)
