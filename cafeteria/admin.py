from django.contrib import admin

from .forms import MenuItemForm
from .models import Category, ContactMessage, GalleryImage, MenuItem, Order, OrderItem, Reservation, Review


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ["menu_item"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm
    list_display = (
        "name",
        "category",
        "price",
        "discounted_price_display",
        "stock_quantity",
        "is_available",
        "is_popular",
        "is_featured",
        "created_at",
    )
    list_filter = ("category", "is_available", "is_popular", "is_featured")
    search_fields = ("name", "description", "ingredients")
    ordering = ("category__name", "name")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Basic Information", {"fields": ("name", "category", "description", "ingredients")}),
        ("Media & Highlights", {"fields": ("image", "is_popular", "is_featured")}),
        ("Nutrition & Prep", {"fields": ("calories", "preparation_time", "rating")}),
        ("Pricing & Availability", {"fields": ("price", "discount_percentage", "stock_quantity", "is_available")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Discounted Price")
    def discounted_price_display(self, obj):
        return f"${obj.discounted_price:.2f}"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "status", "created_at", "total")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "phone_number")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = (OrderItemInline,)
    fieldsets = (
        ("Customer Information", {"fields": ("customer_name", "phone_number")}),
        ("Order Status", {"fields": ("status",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def total(self, obj):
        return obj.total

    total.short_description = "Total"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "menu_item", "quantity", "subtotal")
    list_filter = ("order__status", "menu_item")
    search_fields = ("order__customer_name", "menu_item__name")
    ordering = ("order", "menu_item")
    readonly_fields = ("created_at",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "guests", "reservation_date", "reservation_time", "status")
    list_filter = ("status", "reservation_date")
    search_fields = ("name", "phone", "notes")
    ordering = ("-reservation_date", "reservation_time")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    ordering = ("-created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "rating", "is_published", "created_at")
    list_filter = ("is_published", "rating")
    search_fields = ("customer_name", "review_text")
    ordering = ("-created_at",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "created_at")
    list_filter = ("category", "is_published")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
