from django.db import models

# Create your models here.
class Item(models.Model):
    """Model definition for Item."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Item."""
        name    = models.CharField(max_length=100)
        unit    = models.CharField(max_length=50)
        picture = models.ImageField(upload_to='item_pics/', blank=True, null=True)
        
        def __str__(self):
            return self.name
            
        def stock(self):
            total_in    = self.transaction.filter(transaction_type='IN').agregate(total=models.sum('qty'))['total'] or 0
            total_out   = self.transaction.filter(transaction_type='OUT').agregate(total=models.sum('qty'))['total'] or 0
            return total_in - total_out

        verbose_name = 'Item'
        verbose_name_plural = 'Items'

class Transaction(model.Model):
    TRANSACTION_TYPES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
    ]
    item                = models.ForeignKey(Item, relate_name='transaction', on_delete=models.CASCADE)
    qty                 = models.PositiveIntegerField()
    transaction_type    = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    date                = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.qty})"
