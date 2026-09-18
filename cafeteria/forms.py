from django import forms

from .models import ContactMessage, MenuItem, Order, OrderItem, Reservation


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            "name",
            "category",
            "description",
            "image",
            "ingredients",
            "calories",
            "preparation_time",
            "is_available",
            "is_popular",
            "is_featured",
            "discount_percentage",
            "rating",
            "stock_quantity",
            "price",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "ingredients": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "calories": forms.NumberInput(attrs={"class": "form-control"}),
            "preparation_time": forms.NumberInput(attrs={"class": "form-control"}),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_popular": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "discount_percentage": forms.NumberInput(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control"}),
            "stock_quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data.get("discount_percentage")
        if discount_percentage is not None and discount_percentage > 100:
            raise forms.ValidationError("Discount cannot exceed 100%.")
        return discount_percentage

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and rating > 5:
            raise forms.ValidationError("Rating cannot exceed 5.0.")
        return rating


class OrderItemForm(forms.ModelForm):
    menu_item = forms.ModelChoiceField(
        queryset=MenuItem.objects.filter(is_available=True),
        label="Menu Item",
        empty_label="Select a menu item",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Quantity",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1}),
    )

    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity"]
        widgets = {
            "menu_item": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity is None or quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity

    def clean_menu_item(self):
        menu_item = self.cleaned_data.get("menu_item")
        if menu_item and not menu_item.is_available:
            raise forms.ValidationError("This menu item is currently unavailable.")
        return menu_item


class OrderForm(forms.ModelForm):
    customer_name = forms.CharField(
        max_length=150,
        label="Customer Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your name"}),
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional"}),
    )

    class Meta:
        model = Order
        fields = ["customer_name", "phone_number"]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_customer_name(self):
        customer_name = self.cleaned_data.get("customer_name")
        if customer_name is not None:
            customer_name = customer_name.strip()
            if not customer_name:
                raise forms.ValidationError("Customer name is required.")
        return customer_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number:
            phone_number = phone_number.strip()
        return phone_number


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["name", "phone", "guests", "reservation_date", "reservation_time", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "guests": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "reservation_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "reservation_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Special requests"}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "your@email.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional phone"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "How can we help?"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Tell us about your experience"}),
        }
