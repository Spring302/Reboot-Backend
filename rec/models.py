from django.db import models
from django.contrib.auth.models import User

class Apartments(models.Model):
    name = models.CharField(max_length=50, blank=False)
    users = models.ManyToManyField(User, related_name = 'apartments')

    def __str__(self):
        return self.name


class PriceInfo(models.Model):
    apart = models.ForeignKey(
        Apartments,
        related_name="price_info",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date = models.DateField(auto_now_add=True, blank=False)
    transaction_style = models.CharField(max_length=10, blank=False, default="매매")
    price = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True, default=0
    )

    class Meta:
        ordering = ["date"]
        constraints = [
            models.UniqueConstraint(
                fields=["apart", "date"], name="unique apart price"
            ),
        ]

    def __str__(self):
        return f"{self.transaction_style}, {self.date}, {self.price}, {self.per_price}"
