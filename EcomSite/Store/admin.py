from django.contrib import admin
from Store.models import Customer, Order, OrderItem, Product, Category, Brand

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Brand)
