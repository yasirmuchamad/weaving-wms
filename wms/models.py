from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    """Model definition for Item."""
    name        = models.CharField(max_length=100)
    unit        = models.CharField(max_length=50)
    location    = models.CharField(max_length=50)
    picture     = models.ImageField(upload_to='item_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.name
        
    def stock(self):
        total_in    = self.transactions.filter(transaction_type='IN').aggregate(total=models.Sum('qty'))['total'] or 0
        total_out   = self.transactions.filter(transaction_type='OUT').aggregate(total=models.Sum('qty'))['total'] or 0
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
        return f"{self.name} - {self.leader}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
    ]
    item                = models.ForeignKey(Item, related_name='transactions', on_delete=models.CASCADE)
    qty                 = models.PositiveIntegerField()
    transaction_type    = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    date                = models.DateTimeField(auto_now_add=True)
    requested_by        = models.CharField(max_length = 62, blank=True, null=True)
    received_by         = models.CharField(max_length = 62, blank=True, null=True)
    subdepartement      = models.ForeignKey(Subdepartement, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type} - {self.subdepartement} - {self.item.name} ({self.qty})"
