from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views


admin.autodiscover()

urlpatterns = [    
    path('', views.store, name='store'),
    path('category/<str:category>/', views.category_items, name='category_items'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('create_user/', views.create_user, name='create_user'),
    path('current_orders/', views.current_orders, name='current_orders'),
    path('delete/', views.delete_order, name='delete_order'),
    path('description/<int:product_id>/', views.product_detail, name='product_detail'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('order/<str:transaction_id>/', views.ship_detail, name='ship_detail'),
    path('process_order/', views.processOrder, name='process_order'),
    path('update_item/', views.updateItem, name='update_item'),
    path('update_shipped_status/', views.update_shipped_status, name='update_shipped_status'),

    # path(r'^order/(?P<transaction_id>[0-9].+\.[0-9]{1,2})/$', 'Ecom.my_store.views.ship_detail', name='ship_detail'),
    # path(r'^description/(?P<product_id>[0-9]{1,10})/$', 'Ecom.my_store.views.product_detail', name='product_detail'),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^media/images'),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    
    
]
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)