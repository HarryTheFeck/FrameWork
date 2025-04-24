from django.test import TestCase
from django.contrib.auth import get_user_model
from main.models import Activity, Item, Order, OrderItem, Booking
from django.utils import timezone

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', role='user')
        self.coordinator = User.objects.create_user(username='coordinator', password='password', role='coordinator')
        self.activity = Activity.objects.create(name='Test Activity', description='Test Desc', date='2025-05-01', price=99.99, coordinator=self.coordinator)
        self.item = Item.objects.create(name='Test Item', description='Desc', price=10.00, stock=5)

    def test_booking_creation(self):
        booking = Booking.objects.create(user=self.user, activity=self.activity, date_booked=timezone.now(), status='Confirmed')
        self.assertEqual(booking.user.username, 'testuser')
        self.assertEqual(booking.activity.name, 'Test Activity')

    def test_order_creation(self):
        order = Order.objects.create(user=self.user, total_price=20.00, status='Pending', date_ordered=timezone.now())
        order_item = OrderItem.objects.create(order=order, item=self.item, quantity=2, price=self.item.price)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order.user.username, 'testuser')