from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
  title = models.CharField(max_length=99, blank=False, null=False)
    
  class Meta:
    verbose_name_plural = 'Categories'
  
  def __str__(self):
    return self.title

class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=60, null=True)
  email = models.CharField(max_length=60, null=True)
  phone = models.CharField(max_length=16, null=True)
  
  def __str__(self):
    return self.name
    
class Product(models.Model):
  name = models.CharField(max_length=200, null=True)
  description = models.TextField(blank=True)
  price = models.DecimalField(max_digits=7, decimal_places=2)
  digital = models.BooleanField(default=False, blank=False)
  #image_url = models.CharField(max_length=200, blank=True, null=True)
  image = models.ImageField(upload_to='images', null=True)
  #image_url = models.ImageField(upload_to='images')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
  def __str__(self):
      return self.name
    
class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  date_ordered = models.DateTimeField(auto_now_add=True)
  complete = models.BooleanField(default=False, blank=False)
  transaction_id = models.CharField(max_length=200, null=True)
  # status = models.CharField(max_length=1, choices=STATUS_CHOICES)
  payment_processed = models.BooleanField(default=False, blank=True, null=True)
  status_shipped = models.BooleanField(default=False, blank=False)
  
  def __str__(self):
      return str(self.transaction_id)
  
  @property
  def status(self):
      if self.status_shipped == True:
          return "Shipped"
      elif self.status_shipped == False:
          return "Ship"
      
  @property
  def css_class(self):
      if self.status_shipped == True:
          return "hidden"
      elif self.status_shipped == False:
          return "active"
      
  @property
  def get_cart_total(self):
      orderitems = self.orderitem_set.all()
      total = sum([item.get_total for item in orderitems])
      return total
  
  @property
  def get_cart_items(self):
      orderitems = self.orderitem_set.all()
      total = sum([item.quantity for item in orderitems])
      return total
  
  @property
  def shipping(self):
      shipping = False
      orderitems = self.orderitem_set.all()
      for i in orderitems:
          if i.product.digital == False:
              shipping = True
      return shipping
        
    
class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
  quantity = models.IntegerField(default=0, blank=True, null=True)
  date_added = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
      return self.product.name 
  
  @property
  def get_total(self):
      total = self.product.price * self.quantity
      return total
    
class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
  address = models.CharField(max_length=200, null=True)
  city = models.CharField(max_length=200, null=True)
  state = models.CharField(max_length=200, null=True)
  zipcode = models.CharField(max_length=200, null=True)
  country = models.CharField(max_length=200, null=True)
  
  def __str__(self):
      return self.address
        

  
class Brand(models.Model):
  store_name = models.CharField(max_length=100, null=True, blank=True)
    
  def __str__(self):
    return str(self.store_name)
