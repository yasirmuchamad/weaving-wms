from django.shortcuts import render, redirect
from .models import Item, Subdepartement, Transaction, TransactionItem, Location
from .forms import ItemForm, SubdepartementForm, TransactionForm, TransactionItemForm, TransactionItemFormSet, LocationForm
from django.forms import inlineformset_factory
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction

def location_list(request):
    location = Location.objects.all()

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

def item_list(request):
    items = Item.objects.all()

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

def subdepartement_list(request):
    subdept = Subdepartement.objects.all().order_by('name')

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

def transaction_list(request):
    transaction_item = Transaction.objects.annotate(total_qty=Sum('items__qty')).order_by('-date')
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
