from django.db import models

# Create your models here.
class Item(models.Model):
    """Model definition for Item."""
    name    = models.CharField(max_length=100)
    unit    = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='item_pics/', blank=True, null=True)
    
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

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
    ]
    item                = models.ForeignKey(Item, related_name='transactions', on_delete=models.CASCADE)
    qty                 = models.PositiveIntegerField()
    transaction_type    = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    date                = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.qty})"
