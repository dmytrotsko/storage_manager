from django.shortcuts import render
from indussystem.models import Villa
from .models import *


# Create your views here.
def stm_index(request):
    return render(request, 'storage_manager/stm_index.html')


def villa_list(request):
    villas = Villa.objects.all()

    ctx = {'villas': villas}

    return render(request, 'storage_manager/villa_list.html', ctx)


def villa_details(request, id):
    villa = Villa.objects.get(pk=id)
    items = Item.objects.filter(storage=villa)

    ctx = {'villa': villa,
           'items': items}

    return render(request, 'storage_manager/villa_details.html', ctx)


def create_item(request):
    return render(request, 'storage_manager/create_item.html')


def ajax_search(request):
    q = request.GET['q']
    items = Item.objects.filter(name__icontains=q)
    villas = Villa.objects.filter(name__icontains=q)

    ctx = {'items': items,
           'villas': villas, }

    return render(request, 'storage_manager/ajax_search.html', ctx)
