from .models import Cart

def cart_counter(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items_count = sum(item.quantity for item in cart.items.all())
    else:
        items_count = 0
    return {'cart_items_count': items_count}