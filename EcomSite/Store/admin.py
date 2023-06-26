from django.contrib import admin
from .models import Customer, Order, OrderItem, Product, Category

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)

