from django.contrib import admin
from .models import User, Activity, Booking, Item, Order, OrderItem

admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Booking)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)


### tests/test_models.py ###
from django.test import TestCase
from main.models import User, Activity

class BasicTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass', role='user')
        self.assertEqual(user.username, 'testuser')

    def test_activity_creation(self):
        coordinator = User.objects.create_user(username='coordinator', password='pass', role='coordinator')
        activity = Activity.objects.create(name='Test Activity', description='Test Desc', date='2025-04-24', price=99.99, coordinator=coordinator)
        self.assertEqual(activity.name, 'Test Activity')
