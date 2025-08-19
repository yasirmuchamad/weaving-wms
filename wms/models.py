from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Location(models.Model):
    """Model definition for Location."""

    # TODO: Define fields here
    name = models.CharField(max_length=32)

    class Meta:
        """Meta definition for Location."""

        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        """Unicode representation of Location."""
        return f"{self.name}"


class Item(models.Model):
    """Model definition for Item."""
    name        = models.CharField(max_length=100)
    unit        = models.CharField(max_length=50)
    location    = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name="items")
    picture     = models.ImageField(upload_to='item_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    @property
    def stock(self):
        total_in    = self.transaction_items.filter(transaction__transaction_type='IN').aggregate(total=models.Sum('qty'))['total'] or 0
        total_out   = self.transaction_items.filter(transaction__transaction_type='OUT').aggregate(total=models.Sum('qty'))['total'] or 0
        return total_in - total_out
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for Item."""
        
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

class Subdepartement(models.Model):
    """Model definition for Subdepartement."""

    # TODO: Define fields here
    name    = models.CharField(max_length=32)
    leader  = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        """Meta definition for Subdepartement."""

        verbose_name = 'Subdepartement'
        verbose_name_plural = 'Subdepartements'

    def __str__(self):
        """Unicode representation of Subdepartement."""
        return f"{self.name}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
    ]
    transaction_type    = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    date                = models.DateTimeField(auto_now_add=True)
    requested_by        = models.CharField(max_length = 62, blank=True, null=True)
    received_by         = models.CharField(max_length = 62, blank=True, null=True)
    subdepartement      = models.ForeignKey(Subdepartement, on_delete=models.CASCADE)
    note                = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.subdepartement}"


class TransactionItem(models.Model):
    """Model definition for TransactionItem."""

    # TODO: Define fields here
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    item        = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='transaction_items')
    qty         = models.PositiveIntegerField()
    class Meta:
        """Meta definition for TransactionItem."""

        verbose_name = 'TransactionItem'
        verbose_name_plural = 'TransactionItems'

    def clean(self):
        if self.transaction.transaction_type=="OUT":
            if self.item.stock < self.qty:
                raise ValidationError(
                    f"Stock {self.item.name} not enough."
                    f" Available {self.item.stock}, but your request is {self.qty}."
                )
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of TransactionItem."""
        return f"{self.item.name} {self.qty}"
