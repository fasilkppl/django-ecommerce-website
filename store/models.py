from email.policy import default
from operator import truediv
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)


    def __str__(self):
        return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=10, decimal_places=3)
	digital = models.BooleanField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	warranty_policy = models.CharField(max_length=200, null=True, blank=True)
	brand = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url    

	@staticmethod
	def search(query):
		return Product.objects.filter(name__icontains=query)	
          



class SlideImage(models.Model):
	slideproduct = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='slide_images/')




class OrderCart(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

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
    


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(OrderCart, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total_pdt = self.product.price * self.quantity
		return total_pdt


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(OrderCart, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address







class ReviewItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])



class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )

    item = models.ForeignKey(ReviewItem, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s review of {self.item.name}"









