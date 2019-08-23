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

    if request.method == 'POST':
        # Action
        if request.POST.get('itemTransfer') == '':
            # Transfer item
            item_name = request.POST['item_name_to_transfer']
            price = Item.objects.get(name=item_name, storage_id=id)
            quantity = int(request.POST['quantity'])
            target_storage_id = request.POST['target_storage']

            # Quantity fix
            target_item = Item.objects.get(name=item_name, storage=villa)
            if target_item.quantity <= quantity:
                quantity = target_item.quantity
                target_item.delete()
            else:
                target_item.quantity -= quantity
                target_item.save()

            # Check if target storage has item with the same name
            try:
                old_item = Item.objects.get(name=item_name, storage=target_storage_id)
                old_item.quantity += quantity
                old_item.save()

            # If item was not found, create new one
            except ObjectDoesNotExist:
                Item.objects.create(name=item_name,
                                    quantity=quantity,
                                    storage=Villa.objects.get(pk=target_storage_id),
                                    price=price)

            # Create transaction object for reports
            Transaction.objects.create(item_name=item_name,
                                       quantity=quantity,
                                       price_per_item=price,
                                       user=request.user.id,
                                       type='TR',
                                       storage_from_id=id,
                                       storage_to_id=target_storage_id)

            # Return page with parameters for notification to show up
            return redirect(
                add_parameters(request, transfer=f'{item_name}|{Villa.objects.get(pk=target_storage_id).name}'))

        if request.POST.get('deleteItem') == '':
            # Delete chosen item
            print('delete')
            item = Item.objects.get(name=request.POST['item_name_to_delete'], storage_id=id)
            item_name = item.name

            # Create transaction object for reports
            Transaction.objects.create(item_name=item_name,
                                       quantity=item.quantity,
                                       price_per_item=item.price,
                                       user=request.user.id,
                                       type='DL',
                                       storage_from_id=id,
                                       storage_to=None)

            item.delete()

            # Return page with parameters for notification to show up
            return redirect(add_parameters(request, deleted=f'{item_name}'))

    ctx = {'villa': villa,
           'items': items,
           'villas': villas,
           'transfer': None,
           'transfer_destination': None,
           'deleted': None,
           }

    if request.GET.get('deleted'):
        ctx['deleted'] = request.GET.get('deleted')

    if request.GET.get('transfer'):
        tmp = request.GET.get('transfer').split('|')
        ctx['transfer'] = tmp[0]
        ctx['transfer_destination'] = tmp[1]

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


def reports(request):
    reports = Transaction.objects.all()

    ctx = {
        'reports': reports,
    }

    return render(request, 'storage_manager/reports.html', ctx)


def ajax_reports(request):
    reports = Transaction.objects.all()

    if request.GET['q']:
        reports = reports.filter(item_name__icontains=request.GET['q'])

    if request.GET['report_type']:
        type = request.GET['report_type']
        if type == 'transition':
            reports = reports.filter(type='TR')
        elif type == 'deletion':
            reports = reports.filter(type='DL')
        elif type == 'creation':
            reports = reports.filter(type='CR')
        else:
            ...

        ctx = {'reports': reports}

    return render(request, 'storage_manager/ajax_reports.html', ctx)
