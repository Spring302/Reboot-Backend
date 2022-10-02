from django.db import models


class Apartments(models.Model):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class PriceInfo(models.Model):
    apart = models.ForeignKey(Apartments, related_name='price_info', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0)
    per_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0)

    class Meta:
        ordering = ['date']
        constraints = [
            models.UniqueConstraint(
                fields=['apart', 'date'],
                name="unique aprart price"
            ),
        ]

    def __str__(self):
        return f'{self.date}, {self.price}, {self.per_price}'
