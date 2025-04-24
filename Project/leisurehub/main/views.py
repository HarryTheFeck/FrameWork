from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Activity, Item, Booking, Order, OrderItem
from django.utils import timezone
from django.http import HttpResponseForbidden


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            elif user.role == 'coordinator':
                return redirect('coordinator_activities')
            elif user.role == 'manager':
                return redirect('manage_orders')
            return redirect('dashboard')
        return render(request, 'main/login.html', {'error': 'Invalid credentials'})
    return render(request, 'main/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')


@login_required
def activity_list(request):
    activities = Activity.objects.all()
    return render(request, 'main/activities.html', {'activities': activities})


@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'main/items.html', {'items': items})


@login_required
def book_activity(request, id):
    activity = get_object_or_404(Activity, pk=id)
    Booking.objects.create(user=request.user, activity=activity, date_booked=timezone.now(), status="Confirmed")
    return redirect('activities')


@login_required
def order_item(request, id):
    item = get_object_or_404(Item, pk=id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        total_price = item.price * quantity
        order = Order.objects.create(user=request.user, total_price=total_price, status="Pending", date_ordered=timezone.now())
        OrderItem.objects.create(order=order, item=item, quantity=quantity, price=item.price)
        return redirect('items')
    return render(request, 'main/order_item.html', {'item': item})


# Coordinator-specific views
@login_required
def coordinator_activities(request):
    if request.user.role != 'coordinator':
        return HttpResponseForbidden()
    activities = Activity.objects.filter(coordinator=request.user)
    return render(request, 'main/coordinator_activities.html', {'activities': activities})


@login_required
def create_activity(request):
    if request.user.role != 'coordinator':
        return HttpResponseForbidden()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        price = request.POST.get('price')
        Activity.objects.create(name=name, description=description, date=date, price=price, coordinator=request.user)
        return redirect('coordinator_activities')
    return render(request, 'main/create_activity.html')


# Manager-specific views
@login_required
def manage_orders(request):
    if request.user.role != 'manager':
        return HttpResponseForbidden()
    orders = Order.objects.all().order_by('-date_ordered')
    return render(request, 'main/manage_orders.html', {'orders': orders})


@login_required
def update_order_status(request, order_id):
    if request.user.role != 'manager':
        return HttpResponseForbidden()
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()
    return redirect('manage_orders')
