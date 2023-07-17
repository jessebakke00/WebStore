import json
import time

from django.contrib import messages
from django.contrib.admin.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .utils import cookieCart, cookieData


def create_user(request):
  form = UserCreationForm()
  
  if request.method == 'POST':
    print(request.POST)
    data = {
      'username': request.POST.get('username'),
      'password1': request.POST.get('password1'),
      'password2': request.POST.get('password2')
    }
    form = UserCreationForm(data)
    print(form)
    if form.is_valid():
      form.save()
      user = form.cleaned_data['username']
      messages.success(request, 'New user ' + user + ' was created')
      return redirect('user_login')
    
  context = {
    'form':form
  }
  
  return render(request, 'Store/create_user.html', context)

def cart(request):
  data              = cookieData(request)
  cart_items        = data['cart_items']
  order             = data['order']
  items             = data['items']
  context           = {
    'items':items,
    'order':order,
    'cart_items':cart_items,
    'user':str(request.user)
  }
  
  return render(request, 'Store/cart.html', context)

def checkout(request):
  data              = cookieData(request)
  cart_items        = data['cart_items']
  order             = data['order']
  items             = data['items']    
  context           = {
    'items':items,
    'user': str(request.user),
    'order':order,
    'cart_items':cart_items,
    'shipping':False
  }
  
  return render(request, 'Store/checkout.html', context)

@staff_member_required
def current_orders(request):
  orders            = Order.objects.filter(status_shipped=False)
  order_items       = OrderItem.objects.filter(order__status_shipped=False)
  shipping_address  = ShippingAddress.objects.all()
  context           = {
    'orders':orders,
    'order_items':order_items,
    'user':str(request.user)
  }
  
  return render(request, 'Store/current_orders.html', context)

@csrf_exempt
def delete_order(request):
  
  post_data         = json.loads(request.body.decode())
  print(post_data)
  if request.user.is_authenticated:
    order = Order.objects.get(transaction_id=post_data['orderNumber'])
    order.delete()
  return JsonResponse('Order Deleted', safe=False)



def processOrder(request):
  cart              = json.loads(request.COOKIES['cart'])
  post_data         = json.loads(request.body.decode())
  transaction_id    = time.time()
  
  if request.user.is_authenticated:
    customer        = request.user.customer
    try:
      order, created = Order.objects.get_or_create(customer=customer)
    except:
      order = Order.objects.filter(customer=customer).exclude(payment_processed=True)
      print(order)
  else:
    # print('User is not logged in!!')
      
    name            = post_data['form']['name']
    email           = post_data['form']['email']
    data            = cookieCart(request)
    items           = data['items']
      
    customer, created = Customer.objects.get_or_create(
      email=email
    )
    customer.name = name
    customer.save()      
    
    order = Order.objects.create(
          customer=customer,
          complete=False
    )
      
    for item in items:
      product       = Product.objects.get(id=item['product']['id'])
      orderItem     = OrderItem.objects.create(
        product     = product,
        order       = order,
        quantity    = item['quantity']
      )
  
  total = float(post_data['form']['total'])
  order.transaction_id = transaction_id
  
  if total == float(order.get_cart_total):
    order.complete = True
    order.payment_processed = True
  order.save()

  ShippingAddress.objects.create(
      customer      = customer,
      order         = order,
      address       = post_data['shipping']['address'],
      city          = post_data['shipping']['city'],
      state         = post_data['shipping']['state'],
      zipcode       = post_data['shipping']['zipcode']
  )
  return JsonResponse('Order Processed!!', safe=False)

def product_detail(request, product_id):
  data              = cookieData(request)    
  cart_items        = data['cart_items']
  order             = data['order']
  items             = data['items']
  product           = Product.objects.get(id=product_id)
  context           = {
      'product'   : product,
      'user'      : str(request.user),
      'cart_items': cart_items,
  }
  
  return render(request, 'Store/product_detail.html', context)

@staff_member_required
def ship_detail(request, transaction_id):
  transaction_id    = float(transaction_id)
  order             = Order.objects.get(transaction_id=transaction_id)
  order_items       = OrderItem.objects.filter(order=order)
  shipping_address  = ShippingAddress.objects.get(order=order)
  context = {'order':order, 'shipping_address':shipping_address, 'order_items':order_items, 'user':str(request.user)}
  
  return render(request, 'Store/order_detail.html', context)

def store(request):
  category_list     = Category.objects.all().order_by('title')
  data = cookieData(request)
  cart_items        = data['cart_items']
  order             = data['order']
  items             = data['items']
  products          = Product.objects.all()
  brand             = Brand.objects.get(store_name="Insanitees")
  context           = {
      'category_list': category_list,
      'heading_title': str(brand.store_name),
      'products':products,
      'cart_items':cart_items,
      'user':str(request.user)
  }
  
  return render(request, 'Store/store.html', context)

def category_items(request, category):
  category_list     = Category.objects.all().order_by('title')
  #category          = 
  data              = cookieData(request)
  cart_items        = data['cart_items']
  order             = data['order']
  items             = data['items']
  products          = Product.objects.filter(category__title=category)
  print(products)
  brand             = Brand.objects.get(store_name="Insanitees")
  context           = {
    'category_list': category_list,
    'heading_title': str(brand.store_name),
    'products': products,
    'cart_items': cart_items,
    'user': str(request.user),
  }
  
  return render(request, 'Store/store.html', context)

@csrf_exempt
def updateItem(request):
  # lets get the data posted via ajax 
  data              = json.loads(request.body.decode())
  action            = data['action']
  productId         = data['productId']
  
  # now, lets fetch info from the database using the posted data
  customer           = request.user.customer
  product            = Product.objects.get(id=productId)
  order, created     = Order.objects.get_or_create(customer=customer, complete=False)
  orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
  
  # change quantity
  if action == 'add':
    orderItem.quantity = (orderItem.quantity + 1)
  elif action == 'remove':
    orderItem.quantity = (orderItem.quantity - 1)
  
  # save the updated quantity
  orderItem.save()
  
  # delete if quantity is reduced to 0
  if orderItem.quantity <= 0:
    orderItem.delete()

  return JsonResponse(data, safe=False)

@csrf_exempt
def update_shipped_status(request):
  data      = json.loads(request.body.decode())
  order_num = data['orderNumber']
  order     = Order.objects.get(transaction_id=order_num)
  order.status_shipped = True
  order.save()
  
  return JsonResponse('It workded', safe=False)

def user_login(request):
  if request.user.is_authenticated:
    return redirect('store')
  else:
    form = AuthenticationForm()
    
    if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(username=username, password=password)
    
      if user is not None:
        
        if user.is_active:
          login(request, user)
          return redirect('store')
      else:
        messages.info(request, 'Username or Password is incorrect')
        
    else:
      user = request.user

  context = {'form':form, 'user':user}
  
  return render(request, 'Store/user_login.html', context)

def user_logout(request):
  if request.user.is_authenticated:
    logout(request)
    return redirect('store')
