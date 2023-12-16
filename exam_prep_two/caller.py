import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order


# Create and run your queries within functions
def get_profiles(search_string=None):
    if search_string is None:
        return ''

    profile = Profile.objects.filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profile:
        return ''

    return '\n'.join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profile)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    return '\n'.join(f"Profile: {p.full_name}, orders: {p.orders_count}" for p in profiles)


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ''

    product_names = [p.name for p in last_order.products.all()]

    return f"Last sold products: {', '.join(product_names)}"


def get_top_products():
    top_products = Product.objects.annotate(
        orders_count=Count('order')
    ).filter(orders_count__gt=0).order_by('-orders_count', 'name')[:5]

    if not top_products:
        return ''

    return f"Top products:\n" + '\n'.join(f"{p.name}, sold {p.orders_count} times" for p in top_products)


def apply_discounts():
    orders_count = Order.objects.annotate(
        products_count=Count('products')
    ).filter(
        products_count__gt=2,
        is_completed=False
    ).update(
        total_price=F('total_price') * 0.90
    )

    if not orders_count:
        return "Discount applied to 0 orders."

    return f"Discount applied to {orders_count} orders."


def complete_order():
    order = Order.objects.prefetch_related('products').filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ''

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False
            product.save()

        product.save()

    order.is_completed = True
    order.save()
    return "Order has been completed!"


