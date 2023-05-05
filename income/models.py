from django.db import models

# Create your models here.

class Income(models.Model):
    SOURCE_OPTIONS = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE-HUSTLE', 'SIDE-HUSTLE'),
        ('OTHERS', 'OTHERS')
    ]
    source = models.CharField(max_length=255, choices=SOURCE_OPTIONS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False)

    class Meta:
        ordering = ['-date']
    
    def __str__(self) -> str:
        return str(self.owner) +'s income'




