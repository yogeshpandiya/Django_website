
from tokenize import Number
from django.shortcuts import render,redirect
from .models import *
from . forms import OrderForm

from .filters import OrderFilter
from django.contrib.auth.models import User ,auth
from django.contrib import messages

#------------------------


def index(request):
    return render(request, 'accounts/main.html')

def home(request):
    return render(request, 'accounts/Home.html')

def Login(request):
    return render(request, 'accounts/Login.html')

def SignUp(request):
    return render(request, 'accounts/Signup.html')

def Submit(request):
    if request.method=="POST":
        # Get the post parameters
        FName=request.POST['FName']
        LName=request.POST['LName']
        Email=request.POST['Email']
        username=request.POST['username']
        password=request.POST['password']
        cpassword=request.POST['Cpassword']

        # check for errorneous input
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
            else:
                myuser = User.objects.create_user(username, Email, password)
                myuser.first_name= FName
                myuser.last_name= LName
                myuser.save()
                messages.info(request, "Employee Registered")
        else:
            messages.info(request, 'Password not matching')
            return redirect('/SignUp')
        return redirect('/SignUp')
    else:
        return render(request, 'accounts/Signup.html')

def ULogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user= auth.authenticate(username=username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/dashboard')
        else:
            messages.info(request, "Invalid Credential")
            return render(request, 'accounts/Login.html')
    else:
        return render(request, 'accounts/Login.html')

#def Manager(request):
    #return render(request, 'accounts/dashboard.html')
#-------------------(DETAIL/LIST VIEWS) -------------------

def dashBoard(request):
	orders = Order.objects.all().order_by('-status')[0:5]
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = Order.objects.all().count()
	delivered = Order.objects.filter(status='Delivered').count()
	pending = Order.objects.filter(status='Pending').count()



	context = {'customers':customers, 'orders':orders,
	'total_customers':total_customers,'total_orders':total_orders, 
	'delivered':delivered, 'pending':pending}
	return render(request, 'accounts/dashBoard.html', context)

def products(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'accounts/products.html', context)

def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	total_orders = orders.count()

	orderFilter = OrderFilter(request.GET, queryset=orders) 
	orders = orderFilter.qs

	context = {'customer':customer, 'orders':orders, 'total_orders':total_orders,
	'filter':orderFilter}
	return render(request, 'accounts/customer.html', context)


#-------------------(CREATE VIEWS) -------------------

def createOrder(request):
	action = 'create'
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/dashboard')

	context =  {'action':action, 'form':form}
	return render(request, 'accounts/order_form.html', context)

#-------------------(UPDATE VIEWS) -------------------

def updateOrder(request, pk):
	action = 'update'
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/customer/' + str(order.customer.id))

	context =  {'action':action, 'form':form}
	return render(request, 'accounts/order_form.html', context)

#-------------------(DELETE VIEWS) -------------------

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		customer_id = order.customer.id
		customer_url = '/customer/' + str(customer_id)
		order.delete()
		return redirect(customer_url)
		
	return render(request, 'accounts/delete_item.html', {'item':order})

def create_cst(request):
    return render(request, 'accounts/newcst.html')

def Submit_cst(request):
	if request.method=="POST":
		Name=request.POST['Name']
		Email=request.POST['Email']
		Number=request.POST['Number']
		mycustomers = Customer(name=Name, email=Email , phone=Number)
		mycustomers.save()
	return redirect ('dashboard')

def addproduct(request):
    return render(request, 'accounts/addproduct.html')

def Submit_Product(request):
	if request.method=="POST":
		Name=request.POST['Name']
		if Name == '':
			messages.info(request, "Enter a Valid Name")
			return redirect ('Add_Product/')
		price=request.POST['price']
		print(type(price))
		Number = []
		for i in range(5000):
			b = str(i)
			Number.append(b)
		if price not in(Number):
			messages.info(request, "Enter a Valid Price between 0-5000")
			return redirect ('Add_Product/')
		category=request.POST['category']
		if category == '':
			messages.info(request, "Enter a Valid Category, Hint: South Indian/Italian/Chinees etc")
			return redirect ('Add_Product/')
		description=request.POST['description']
		if description == '':
			messages.info(request, "Enter a Valid Description, Hint; Veg/Non-Veg etc.")
			return redirect ('Add_Product/')
		
		else:
			myproduct = Product(name=Name, price=price , description=description, category=category)
			myproduct.save()
			return redirect ('dashboard')
