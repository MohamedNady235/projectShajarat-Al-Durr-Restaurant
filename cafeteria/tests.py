from django.test import TestCase
from django.urls import reverse


class RestaurantPagesTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_about_page_loads(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_gallery_page_loads(self):
        response = self.client.get(reverse("gallery"))
        self.assertEqual(response.status_code, 200)

    def test_reservation_page_loads(self):
        response = self.client.get(reverse("reserve-table"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
