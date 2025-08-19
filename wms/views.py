from django.shortcuts import render, redirect
from .models import Item, Transaction, TransactionItem
from .forms import ItemForm, TransactionForm, TransactionItemForm, TransactionItemFormSet
from django.forms import inlineformset_factory
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction

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
    return render(request, 'wms/item/item_form.html', {'form': form})

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
                                    f"Stock {item.item.name} not enough! (ready stock : {item.item.stock})."
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
        'forms':transaction_form,
        'formset':formset
    }

    return render(request, 'wms/transaction/transaction_form.html', context)
