from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Activity, Item

User = get_user_model()

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='password', role='user')
        self.activity = Activity.objects.create(name='Activity Test', description='Desc', date='2025-05-01', price=100.0, coordinator=self.user)
        self.item = Item.objects.create(name='Item Test', description='Item Desc', price=15.0, stock=10)

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_activities_page(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('activities'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Activity Test')

    def test_items_page(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('items'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item Test')
