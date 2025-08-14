from django import forms
from models import Item, Transaction

class ItemForm(forms.ModelForm):
    """Form definition for Item."""

    class Meta:
        """Meta definition for Itemform."""

        model = Item
        fields = ['name', 'unit', 'picture']

class TransactionForm(forms.ModelForm):
    """Form definition for Transaction."""

    class Meta:
        """Meta definition for Transactionform."""

        model = Transaction
        fields = ['item', 'qty', 'transaction_type']
