from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Subdepartement, Transaction, TransactionItem, Location
from .forms import ItemForm, SubdepartementForm, TransactionForm, TransactionItemForm, TransactionItemFormSet, LocationForm
from django.forms import inlineformset_factory
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

def location_list(request):
    locations = Location.objects.all().order_by('name')

    paginator = Paginator(locations, 10)
    page_number = request.GET.get('page')
    location = paginator.get_page(page_number)

    context = {
        'title':'List Location',
        'locations':location,
    }
    return render(request, 'wms/location/location_list.html', context)

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wms:location_list')
    else:
        form = LocationForm()
    context = {
        'title':'Form Location',
        'form':form
    }

    return render(request, 'wms/location/location_form.html', context)

def update_location(request, pk):
    location = get_object_or_404(Location, pk=pk)

    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('wms:location_list')
    else:
        form = LocationForm(instance=location)

    context = {
        'title': 'Update Location',
        'form': form
    }
    return render(request, 'wms/location/location_form.html', context)

def delete_location(request, pk):
    location = get_object_or_404(Location, pk=pk)

    if request.method == 'POST':
        location.delete()
    return redirect('wms:location_list')

def export_locationToExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "List Location"

    # Judul besar di baris 1
    ws.merge_cells('A1:G1')  # gabungkan dari kolom A sampai B
    ws['A1'] = "List Location"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Header
    headers = ['Id', 'Name']
    ws.append(headers)

    # Data
    for idx, s in enumerate(Location.objects.all(), start=1):
        ws.append([
            idx,
            s.name,
        ])

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Location.xlsx'
    wb.save(response)
    return response
    
def item_list(request):
    item_lists = Item.objects.all().order_by('name')

    paginator = Paginator(item_lists, 10)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)

    context = {
        'title':'List Item',
        'items':items,
    }
    return render(request, 'wms/item/item_list.html', context)

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('wms:item_list')
    else:
        form = ItemForm()
    
    context = {
        'title':'Form Item',
        'form':form,
    }
    return render(request, 'wms/item/item_form.html', context)

def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('wms:item_list')
    else:
        form = ItemForm(instance=item)

    context = {
        'title': 'Update Item',
        'form': form
    }
    return render(request, 'wms/item/item_form.html', context)

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        item.delete()
    return redirect('wms:item_list')

def export_itemToExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "List Item"

    # Judul besar di baris 1
    ws.merge_cells('A1:G1')  # gabungkan dari kolom A sampai B
    ws['A1'] = "List Item"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Header
    headers = ['Id', 'Name', 'Unit', 'Location', 'Picture', 'Stock']
    ws.append(headers)

    # Data
    for idx, s in enumerate(Item.objects.all(), start=1):
        ws.append([
            idx,
            s.name,
            s.unit,
            s.location.name,
            str(s.picture.url if s.picture else ""),  # konversi ke string
            s.stock,
        ])

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Item.xlsx'
    wb.save(response)
    return response

def subdepartement_list(request):
    subdepts = Subdepartement.objects.all().order_by('name')

    paginator = Paginator(subdepts, 10)
    page_number = request.GET.get('page')
    subdept = paginator.get_page(page_number)

    context = {
        'title':'List Sub-Departement',
        'subdepts':subdept,
    }
    return render(request, 'wms/subdept/subdept_list.html', context)

def add_subdepartement(request):
    if request.method == 'POST':
        form = SubdepartementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wms:subdept_list')
    else:
        form = SubdepartementForm()
    
    context = {
        'title':'Form Sub-Departement',
        'form':form,
    }
    return render(request, 'wms/subdept/subdept_form.html', context)

def update_subdepartement(request, pk):
    subdept = get_object_or_404(Subdepartement, pk=pk)

    if request.method == 'POST':
        form = SubdepartementForm(request.POST, instance=subdept)
        if form.is_valid():
            form.save()
            return redirect('wms:subdept_list')
    else:
        form = SubdepartementForm(instance=subdept)

    context = {
        'title': 'Update Sub-Departement',
        'form': form
    }
    return render(request, 'wms/subdept/subdept_form.html', context)

def delete_subdepartement(request, pk):
    subdept = get_object_or_404(Subdepartement, pk=pk)

    if request.method == 'POST':
        subdept.delete()
    return redirect('wms:subdept_list')


def export_subdeptToExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "List Sub-Departement"

    # Judul besar di baris 1
    ws.merge_cells('A1:G1')  # gabungkan dari kolom A sampai B
    ws['A1'] = "List Sub-Departement"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Header
    headers = ['Id', 'Name', 'Leader']
    ws.append(headers)

    # Data
    for idx, s in enumerate(Subdepartement.objects.all(), start=1):
        ws.append([
            idx,
            s.name,
            s.leader,
        ])

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Subdept.xlsx'
    wb.save(response)
    return response


def transaction_list(request):
    transaction_item = Transaction.objects.annotate(total_qty=Sum('items__qty')).order_by('-date')

    paginator = Paginator(transaction_item, 10)
    page_number = request.GET.get('page')
    transaction_item = paginator.get_page(page_number)

    context = {
         'title':"List Transaction",
         'transactions' : transaction_item
     }
    return render(request, 'wms/transaction/transaction_list.html', context)

def add_transaction(request):
    TransactionItemFormSet = inlineformset_factory(
        Transaction, TransactionItem, form=TransactionItemForm, extra=1, can_delete=True
    )
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        formset = TransactionItemFormSet(request.POST)

        if transaction_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    transaction_obj = transaction_form.save()
                    has_error =False
                    items = formset.save(commit=False)

                    for form in formset.forms:
                        item = form.save(commit=False)
                        if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                            continue

                        item = form.save(commit=False)
                        item.transaction = transaction_obj

                        if transaction_obj.transaction_type =="OUT":
                            if item.qty > item.item.stock:
                                form.add_error(
                                    "qty",
                                    f"Stock {item.item.name} is not enough! (ready stock : {item.item.stock})."
                                )
                                has_error = True
                                continue
                        try:
                            item.full_clean()
                        except ValidationError as e:
                            for msg in e.messages:
                                form.add_error(None, msg)

                        item.save()
                    
                    formset.save_m2m()

                    if has_error:
                        raise ValidationError("Ada error pada item formset")
                if not has_error:
                    messages.success(request, "Transaction succesfully created.")
                    return redirect('wms:transaction_list')
                
            except ValidationError:
                pass

    else:
        transaction_form = TransactionForm()
        formset = TransactionItemFormSet()

    context = {
        'title':'Form Transaction',
        'forms':transaction_form,
        'formset':formset
    }

    return render(request, 'wms/transaction/transaction_form.html', context)

def export_transaksiToExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "List Transaksi"

    # Judul besar di baris 1
    # ws.merge_cells('A1:G1')  # gabungkan dari kolom A sampai B
    # ws['A1'] = "List Transaksi"
    # ws['A1'].font = Font(size=14, bold=True)
    # ws['A1'].alignment = Alignment(horizontal='center')

    # Header
    headers = ['Id', 'Date', 'Type', 'requested_by', 'received_by', 'Sub-departement', 'Item', 'Qty']
    ws.append(headers)

    # Data
    row_num = 2
    transactions = Transaction.objects.prefetch_related("items__item").all().order_by("-date")
    for idx, trx in enumerate(transactions, start=1):
        if trx.items.exists():
            for trx_item in trx.items.all():
                ws.append([
                    idx,
                    trx.date.strftime("%Y-%m-%d %H:%M"),
                    trx.transaction_type,
                    trx.requested_by,
                    trx.received_by,
                    trx.subdepartement.name,
                    trx_item.item.name,
                    trx_item.qty,
                    trx.note,
                ])
        else:
            ws.append([
                idx,
                    trx.date.strftime("%Y-%m-%d %H:%M"),
                    trx.transaction_type,
                    trx.requested_by,
                    trx.received_by,
                    trx.subdepartement.name,
                    "-",
                    0,
                    trx.note,
                ])
        
        for col in ws.columns:
            max_length = 0
            column = col[0].column
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            ws.column_dimensions[get_column_letter(column)].width = max_length + 2

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Transaction.xlsx'
    wb.save(response)
    return response