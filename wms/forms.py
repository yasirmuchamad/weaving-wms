from django import forms
from django.forms import inlineformset_factory
from .models import Item, Transaction, TransactionItem

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
        fields = ['transaction_type', 'requested_by', 'received_by', 'subdepartement', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # field yang akan ditampilkan
        self.fields['transaction_type'].widget.attrs.update({'id':'transaction_type', 'name':'transaction_type',
                'class':'form-select'}) 
        self.fields['requested_by'].widget.attrs.update({'id':'requested_by', 'name':'requested_by',
                'class':'form-control'})
        self.fields['received_by'].widget.attrs.update({'id':'received_by', 'name':'received_by',
                'class':'form-control'})
        self.fields['subdepartement'].widget.attrs.update({'id':'subdepartement', 'name':'subdepartement',
                'class':'form-select'})
        self.fields['note'].widget.attrs.update({'id':'note', 'name':'note',
                'class':'form-control', 'style':'height:230px;'})
        
    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get("transaction_type")
        requested_by = cleaned_data.get("requested_by")
        received_by = cleaned_data.get("received_by")

        if transaction_type == "IN":
            if not received_by:
                raise forms.ValidationError('Received by wajib diisi untuk transaksi IN.')
            cleaned_data["requested_by"] = None
        
        elif transaction_type == "OUT":
            if not requested_by:
                raise forms.ValidationError('Requested by wajib diisi untuk transaksi OUT.')
            cleaned_data["received_by"] = None

        return cleaned_data
    
class TransactionItemForm(forms.ModelForm):
        """Form definition for TransactionItem."""

        class Meta:
                """Meta definition for TransactionItemform."""

                model = TransactionItem
                fields = ['item', 'qty']
        
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                # field yang akan ditampilkan
                self.fields['item'].widget.attrs.update({'id':'item', 'name':'item',
                        'class':'form-select'}) 
                self.fields['qty'].widget.attrs.update({'id':'qty', 'name':'qty',
                        'class':'form-control'})

TransactionItemFormSet = inlineformset_factory(
     Transaction, TransactionItem,
     form=TransactionItemForm,
     extra=1,
     can_delete=True
)