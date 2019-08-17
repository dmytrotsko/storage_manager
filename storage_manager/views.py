from django.shortcuts import render
from indussystem.models import Villa
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from indussystem.parameters import add_parameters
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def stm_index(request):
    return render(request, 'storage_manager/stm_index.html')


def villa_list(request):
    villas = Villa.objects.all()
    paginator = Paginator(villas, 25)

    page = request.GET.get('page')
    villas = paginator.get_page(page)

    ctx = {'villas': villas}

    return render(request, 'storage_manager/villa_list.html', ctx)


def villa_details(request, id):
    villa = Villa.objects.get(pk=id)
    items = Item.objects.filter(storage=villa)
    villas = Villa.objects.exclude(pk=id)

    # print(a)

    if request.method == 'POST':
        if request.POST.get('transferItem'):
            item_name = request.POST['item_name_to_transfer']
            quantity = int(request.POST['quantity'])
            target_storage_id = request.POST['target_storage']

            target_item = Item.objects.get(name=item_name, storage=villa)
            if target_item.quantity <= quantity:
                quantity = target_item.quantity
                target_item.delete()
            else:
                target_item.quantity -= quantity
                target_item.save()

            try:
                old_item = Item.objects.get(name=item_name, storage=target_storage_id)
                old_item.quantity += quantity
                old_item.save()

            except ObjectDoesNotExist:
                Item.objects.create(name=item_name,
                                    quantity=quantity,
                                    storage=Villa.objects.get(pk=target_storage_id))

        if request.POST.get('deleteItem') == '':
            print('delete')
            item_name = request.POST['item_name_to_delete']
            Item.objects.get(name=item_name, storage=id).delete()

    ctx = {'villa': villa,
           'items': items,
           'villas': villas}

    return render(request, 'storage_manager/villa_details.html', ctx)


def create_item(request):
    villas = Villa.objects.all()

    if request.method == 'POST':
        item_name = request.POST['item_name']
        item_storage_id = request.POST['item_storage']
        item_quantity = int(request.POST['item_quantity'])

        try:
            item = Item.objects.get(name=item_name, storage=Villa.objects.get(pk=item_storage_id))
            item.quantity += item_quantity
            item.save()
        except ObjectDoesNotExist:
            Item.objects.create(name=item_name,
                                storage=Villa.objects.get(pk=item_storage_id),
                                quantity=item_quantity)

        return redirect(add_parameters(request, item=item_name))

    ctx = {'villas': villas,
           'item': None}

    if request.GET.get('item'):
        ctx['item'] = request.GET.get('item')

    return render(request, 'storage_manager/create_item.html', ctx)


def ajax_search(request):
    q = request.GET['q']
    items = Item.objects.filter(name__icontains=q)
    villas = Villa.objects.filter(name__icontains=q)

    ctx = {'items': items,
           'villas': villas, }

    return render(request, 'storage_manager/ajax_search.html', ctx)
