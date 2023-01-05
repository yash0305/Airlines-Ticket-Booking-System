from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(flight  , cart):
    print(flight, cart)
    keys = cart.keys()
    for id in keys:
        if int(id) == flight.id:
            return True
    return False;


@register.filter(name='cart_quantity')
def cart_quantity(flight  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == flight.id:
            return cart.get(id)
    return 0;


@register.filter(name='price_total')
def price_total(flight  , cart):
    return flight.Price * cart_quantity(flight , cart)


@register.filter(name='total_cart_price')
def total_cart_price(flight , cart):
    sum = 0 ;
    for p in flight:
        sum += price_total(p , cart)

    return sum
    