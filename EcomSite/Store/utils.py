import json
from .models import *
from django.views.decorators.csrf import csrf_exempt


def cookieCart(request):
  try:
    cookies = request.META['HTTP_COOKIE'].split(';')
    # print(cookies)
    for cookie in cookies:
      c = str(cookie).strip()
      if c.startswith('cart'):
        print(c)
        cart = json.loads(c[5:])
        print(cart)
      else:
        cart = {}

      items = []
      order = {'get_cart_items':0, 'get_cart_total':0}
      cart_items = order['get_cart_items']
    

      for i in cart.keys():
        # print('cart: ', i, cart[i])
        print(i, cart[i])
        cart_items += cart[i]['quantity']
        print('cart_items: ', cart_items)
        product = Product.objects.get(id=i)
        print('product: ', product)
        total = product.price * cart[i]['quantity']
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']
        print('order: ', order)
        item = {
          'product': {
          'id': product.id,
          'name': product.name,
          'price': product.price,
          'image_url': product.image.url
          },
        'quantity': cart[i]['quantity'],    
        }
        for key in item.keys():
          print('item: ', key, item[key])
        print('item: ', item)
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