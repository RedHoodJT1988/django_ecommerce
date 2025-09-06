from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Product(models.Model):
    name: models.CharField = models.CharField(max_length=200)
    description: models.TextField = models.TextField(blank=True)
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    image: models.ImageField = models.ImageField(
        upload_to="products/", blank=True, null=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("store:product_detail", args=[self.id])


class Order(models.Model):
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    is_paid: models.BooleanField = models.BooleanField(default=False)
    stripe_payment_intent: models.CharField = models.CharField(
        max_length=255, blank=True, null=True
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order: models.ForeignKey = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product: models.ForeignKey = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity: models.PositiveIntegerField = models.PositiveIntegerField(default=1)
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product.name}"
