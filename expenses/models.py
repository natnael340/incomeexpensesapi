from django.db import models

# Create your models here.

class Expense(models.Model):
    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('TRAVEL', 'TRAVEL'),
        ('FOOD', 'FOOD'),
        ('RENT', 'RENT'),
        ('TRANSPORTATION', 'TRANSPORTATION'),
        ('BILLS', 'BILLS'),
        ('OTHERS', 'OTHERS')
    ]
    category = models.CharField(max_length=255, choices=CATEGORY_OPTIONS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False)

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return str(self.owner) +'s income'


