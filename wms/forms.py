from django import forms
from .models import Item, Transaction

class ItemForm(forms.ModelForm):
    """Form definition for Item."""

    class Meta:
        """Meta definition for Itemform."""

        model = Item
        fields = ['name', 'unit', 'location', 'picture']

    def __init__(self, *args, **KWarg):
        super(ItemForm, self).__init__(*args, **KWarg)
        self.fields['name'].widget.attrs.update({'id':'name', 'name':'name',
                'class':'form-control'}) 
        self.fields['unit'].widget.attrs.update({'id':'unit', 'name':'unit',
                'class':'form-control'})
        self.fields['location'].widget.attrs.update({'id':'location', 'name':'location',
                'class':'form-control'}) 
        self.fields['picture'].widget.attrs.update({'id':'picture', 'name':'picture',
                'class':'form-control'}) 

class TransactionForm(forms.ModelForm):
    """Form definition for Transaction."""

    class Meta:
        """Meta definition for Transactionform."""

        model = Transaction
        fields = ['item', 'qty', 'transaction_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # filter field berdasarkan tipe Transaksi
        if self.instance and self.instance.transaction_type == "IN":
            self.fields['requested_by'].widget = forms.HiddenInput()
        elif self.instance and self.instance.transaction_type == "OUT":
            self.fields['received_by'].widget = forms.HiddenInput()