from django.shortcuts import render , get_object_or_404
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cartData,guestOrder
from django.core.paginator import Paginator

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product, Review
from .forms import ReviewForm



def store(request):
	cartDatA = cartData(request)
	cartItems = cartDatA['cartItems']
	context ={"cartItems" : cartItems}
	return render(request, 'store/index.html', context)






def shop(request):
    # Get cart items count
    cart_data = cartData(request)
    cart_items = cart_data['cartItems']
    
    # Get all products
    products = Product.objects.all()

    # Pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Search feature
    query = request.GET.get('q')
    if query:
        search_results = Product.search(query)
        paginator = Paginator(search_results, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        search_results = []



    context = {
        'products': products,
        'cartItems': cart_items,
        'page_obj': page_obj,
        'search_results': search_results,
        'query': query,
    }
    return render(request, 'store/shop.html', context)





def shop_single(request, pk):
    product = get_object_or_404(Product, pk=pk)
    products=Product.objects.all()

    slideimages = SlideImage.objects.filter(slideproduct=product)
    cart_data = cartData(request)
    cart_items = cart_data['cartItems']
     # Get all images related to the product
    context = {
        'product': product,
		'cartItems': cart_items,
        'slideimages': slideimages,
        'products':products
      
    }
    return render(request, 'store/shop-single.html', context)








def cart(request):
	cartDatA = cartData(request)
	cartItems = cartDatA['cartItems']  #in utils.py we are returning a dictionary ,so we are accessing it using key/value pairs
	order = cartDatA['order']
	items = cartDatA['items']

	context = {'items':items, 'order':order,"cartItems" : cartItems}	
	return render(request, 'store/cart.html',context)





def checkout(request):

	cartDatA = cartData(request)
	cartItems = cartDatA['cartItems']  #in utils.py we are returning a dictionary ,so we are accessing it using key/value pairs
	order = cartDatA['order']
	items = cartDatA['items']

	context = {'items':items, 'order':order,"cartItems" : cartItems}	
	return render(request, 'store/checkout.html',context)




def updateItem(request):
	
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId) #using this line,we can use product. in templates 
    order, created = OrderCart.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def processOrder(request):

	transaction_id = datetime.datetime.now().timestamp() #setting transaction id.
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = OrderCart.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request,data) #in utils.py in def guestOrder we return customer, order


	total = float(data['form']['total'])
	order.transaction_id = transaction_id  #order is from models.py
	
	#checking total (from frontend) == total (from backend) -- to increase security.
	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)


	return JsonResponse('Payment complete..', safe=False)







def item_detail(request, pk):
    item = get_object_or_404(ReviewItem, pk=pk)
    reviews = item.reviews.order_by('-id')
    context = {
        'item': item,
        'reviews': reviews,
    }
    return render(request, 'store/item_detail.html', context)


def add_review(request, pk):
    item = get_object_or_404(ReviewItem, pk=pk)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.item = item
        review.save()
        messages.success(request, 'Your review was submitted successfully.')
        return HttpResponseRedirect(reverse('item-detail', args=[str(item.pk)]))
    context = {
        'item': item,
        'form': form,
    }
    return render(request, 'store/add_review.html', context)








from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    context = {
        'title': 'Contact Us',
        'styles': [
            'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
        ]
    }
    if request.method == 'POST':
        email = request.POST.get('email', '')
        title = request.POST.get('title', '')
        complaint = request.POST.get('complaint', '')
        if email and title and complaint:
            message = f'Title: {title}\nEmail: {email}\n\n{complaint}'
            send_mail(
                'New Contact Request',
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['fasilkppl@gmail.com'],
                fail_silently=False,
            )
            context['success'] = 'Your message has been sent. Thank you for contacting us!'
        else:
            context['error'] = 'Please fill in all required fields.'
    return render(request, 'store/contact.html', context)





