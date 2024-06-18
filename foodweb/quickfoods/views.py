from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from .forms import  CartItemForm, FoodItemForm
from .models import profile
from .models import FoodItem, Cart, CartItem

# Create your views here.
from .models import FoodItem


@login_required(login_url ='signin.html')
def index(request):
    food_items = FoodItem.objects.all()
    return render(request, 'index.html', {'food_items': food_items})
   

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password ==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and dirfect into settings page

                #crete profile object for the user
                user_model = User.objects.get(username=username)
                new_profile = profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('signup.html')


        else:
            messages.info(request,'passwords not marching')
            return redirect('signup.html')

    else:
        return render(request,'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password= password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin.html')

    else:
        return render(request, 'signin.html')

@login_required(login_url ='signin.html')
def logout(request):
    auth.logout(request)
    return redirect('signin.html')


'''def add_to_cart(request, food_id):
    food_item = FoodItem.objects.get(pk=food_id)
    cart = request.session.get('cart', {})
    cart[food_id] = {
        'name': food_item.name,
        'price': float(food_item.price),
        'quantity': cart.get(food_id, {}).get('quantity', 0) + 1
    }
    request.session['cart'] = cart
    return redirect('index.html')'''

@login_required
def add_to_cart(request, id):
    food = get_object_or_404(FoodItem, id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food=food)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart.html')


'''

def cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = cart.total_price
    for id, item in cart.cart():
        total_price += item['price'] * item['quantity']
        cart_items.append({
            'id': id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity']
        })
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = cart.total_price
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
'''

@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url='signin.html')
def create_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save()
            food_item.save()
            return redirect('index.html')
    else:
        form = FoodItemForm()
    return render(request, 'create_food_item.html', {'form': form})



