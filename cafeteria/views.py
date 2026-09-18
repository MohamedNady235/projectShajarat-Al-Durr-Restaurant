from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm, OrderForm, OrderItemForm, ReservationForm
from .models import Category, GalleryImage, MenuItem, Order, OrderItem, Reservation, Review


def home(request):
    categories = Category.objects.filter(is_active=True).prefetch_related("menu_items")
    featured_items = MenuItem.objects.filter(is_available=True, is_featured=True).select_related("category")[:6]
    popular_items = MenuItem.objects.filter(is_available=True, is_popular=True).select_related("category")[:4]
    reviews = Review.objects.filter(is_published=True)[:6]
    gallery_images = GalleryImage.objects.filter(is_published=True)[:6]
    context = {
        "categories": categories,
        "featured_items": featured_items,
        "popular_items": popular_items,
        "reviews": reviews,
        "gallery_images": gallery_images,
        "page_title": "Shajarat Al-Durr Restaurant",
    }
    return render(request, "home.html", context)


def menu_list(request):
    categories = Category.objects.filter(is_active=True)
    menu_items = MenuItem.objects.filter(is_available=True).select_related("category")
    if request.GET.get("category"):
        menu_items = menu_items.filter(category__name__iexact=request.GET["category"])
    if request.GET.get("q"):
        menu_items = menu_items.filter(name__icontains=request.GET["q"])
    context = {
        "categories": categories,
        "menu_items": menu_items,
        "page_title": "Our Menu",
    }
    return render(request, "menu_list.html", context)


def menu_detail(request, menu_item_id):
    menu_item = get_object_or_404(
        MenuItem.objects.select_related("category"),
        pk=menu_item_id,
        is_available=True,
    )
    context = {
        "menu_item": menu_item,
        "page_title": menu_item.name,
    }
    return render(request, "menu_detail.html", context)


def place_order(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        order_item_form = OrderItemForm(request.POST)

        if order_form.is_valid() and order_item_form.is_valid():
            order = order_form.save()
            order_item = order_item_form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect("order_confirmation", order_id=order.pk)
    else:
        order_form = OrderForm()
        order_item_form = OrderItemForm()

    context = {
        "order_form": order_form,
        "order_item_form": order_item_form,
        "page_title": "Place Your Order",
    }
    return render(request, "place_order.html", context)


def about(request):
    reviews = Review.objects.filter(is_published=True)[:4]
    return render(request, "about.html", {"page_title": "About Us", "reviews": reviews})


def gallery(request):
    images = GalleryImage.objects.filter(is_published=True)
    return render(request, "gallery.html", {"page_title": "Gallery", "images": images})


def reserve_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reserve-table")
    else:
        form = ReservationForm()
    return render(request, "reserve_table.html", {"page_title": "Reserve Table", "form": form})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"page_title": "Contact Us", "form": form})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items__menu_item"), pk=order_id)
    context = {
        "order": order,
        "page_title": "Order Confirmation",
    }
    return render(request, "order_confirmation.html", context)


# Backward-compatible alias
index = home
