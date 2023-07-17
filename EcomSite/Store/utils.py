import json
from .models import *
from django.views.decorators.csrf import csrf_exempt


def cookieCart(request):
  try:
    cookies = request.META['HTTP_COOKIE'].split(';')

    for cookie in cookies:
      c = str(cookie).strip()
      if c.startswith('cart'):
        cart = json.loads(c[5:])
      else:
        cart = {}

      items = []
      order = {'get_cart_items':0, 'get_cart_total':0}
      cart_items = order['get_cart_items']
    

      for i in cart.keys():
        cart_items += cart[i]['quantity']
        product = Product.objects.get(id=i)
        total = product.price * cart[i]['quantity']
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']
        item = {
          'product': {
          'id': product.id,
          'name': product.name,
          'price': product.price,
          'image': {
             'url': product.image.url
            }
          },
        'quantity': cart[i]['quantity'],
        }
        items.append(item)
  except:
    cart_items = 0
    order = {'cart_total':0, 'cart_items':0}
    items = []
  
  return {'cart_items':cart_items, 'order':order, 'items':items}


def cookieData(request):
  if request.user.is_authenticated:
    try:
      customer = request.user.customer
    except:
      customer = Customer(user=request.user, name=request.user, email="")
      customer.save()
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cart_items = order.get_cart_items
  else:
    cookieData = cookieCart(request)
    cart_items = cookieData['cart_items']
    order      = cookieData['order']
    items      = cookieData['items']
    
  return {'cart_items':cart_items, 'order':order, 'items':items}
