from django.shortcuts import render, redirect
from .models import Item, Transaction
from .forms import ItemForm, TransactionForm

def item_list(request):
    items = Item.objects.all()
    return render(request, 'wms/item_list.html', {'items': items})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('wms:item_list')
    else:
        form = ItemForm()
    return render(request, 'wms/item_form.html', {'form': form})

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wms:item_list')
    else:
        form = TransactionForm()
    return render(request, 'wms/transaction_form.html', {'form': form})
