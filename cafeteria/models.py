from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="menu_items",
    )
    name = models.CharField(max_length=150, unique=True, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="menu_images/", blank=True, null=True)
    ingredients = models.TextField(blank=True)
    calories = models.PositiveIntegerField(default=0)
    preparation_time = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    discount_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=Decimal("4.5"),
        validators=[MinValueValidator(Decimal("0.0")), MaxValueValidator(Decimal("5.0"))],
    )
    stock_quantity = models.PositiveIntegerField(default=10, validators=[MinValueValidator(0)])
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ["category__name", "name"]

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip()
        if self.price is not None and self.price < Decimal("0.01"):
            raise ValidationError({"price": "Price must be at least 0.01."})
        if self.discount_percentage is not None and self.discount_percentage > 100:
            raise ValidationError({"discount_percentage": "Discount cannot exceed 100%."})
        if self.rating is not None and self.rating > Decimal("5.0"):
            raise ValidationError({"rating": "Rating cannot exceed 5.0."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount_percentage:
            return self.price * (Decimal("1") - (Decimal(self.discount_percentage) / Decimal("100")))
        return self.price

    @property
    def has_discount(self):
        return self.discount_percentage > 0

    @property
    def rating_stars(self):
        full_stars = int(self.rating)
        half_star = self.rating - Decimal(full_stars) >= Decimal("0.5")
        if half_star:
            full_stars += 1
        empty_stars = 5 - full_stars
        return "⭐" * full_stars + "☆" * max(empty_stars, 0)

    @property
    def in_stock(self):
        return self.stock_quantity > 0

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_PREPARING = "Preparing"
    STATUS_READY = "Ready"
    STATUS_DELIVERED = "Delivered"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PREPARING, "Preparing"),
        (STATUS_READY, "Ready"),
        (STATUS_DELIVERED, "Delivered"),
    ]

    customer_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def clean(self):
        super().clean()
        if not self.customer_name or not self.customer_name.strip():
            raise ValidationError({"customer_name": "Customer name is required."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def total(self):
        return sum((item.subtotal for item in self.items.all()), Decimal("0.00"))

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["order", "menu_item"]
        constraints = [
            models.UniqueConstraint(fields=["order", "menu_item"], name="unique_order_menu_item")
        ]

    def clean(self):
        super().clean()
        if self.quantity < 1:
            raise ValidationError({"quantity": "Quantity must be at least 1."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"


class Reservation(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    guests = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1)])
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="Pending", choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.reservation_date}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'Message'}"


class Review(models.Model):
    customer_name = models.CharField(max_length=150)
    review_text = models.TextField()
    rating = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    avatar_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-created_at"]

    def __str__(self):
        return self.customer_name


class GalleryImage(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="gallery_images/")
    category = models.CharField(max_length=50, default="Dining")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
