from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderCart)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ReviewItem)
admin.site.register(SlideImage)