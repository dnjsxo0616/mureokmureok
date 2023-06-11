from alarms.models import BroadcastAlarm
from sales.models import Product
from decimal import Decimal


def alarms(request):
    allalarms = BroadcastAlarm.objects.all()
    return {'alarms': allalarms}


def carts(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for product_pk, product_info in cart.items():
        product = Product.objects.get(pk=product_pk)
        
        total_price = Decimal(product_info['quantity']) * product.price
        cart_total += total_price
        cart_items.append({
            'product': product,
            'quantity': product_info['quantity'],
            'total_price': total_price,
        })

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return (context)