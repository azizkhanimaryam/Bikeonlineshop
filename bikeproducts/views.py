from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, Cart, CartItem, Payment
from .forms import productForm, LoginForm, PaymentForm
from django.contrib.auth import authenticate, login
from django.conf import settings
#import stripe

#stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request=request, template_name="index.html")

def about(request):
    return render(request=request, template_name="about.html")

def contact(request):
    return render(request=request, template_name="contact.html")

def shop(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop.html', context)


def product_list(request):
    products = Product.objects.filter(available=True)
    context = {
        'products': products
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, id):
    products = get_object_or_404(Product, id=id, available=True)
    context = {
        'products': products
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def view_cart(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = cart.cartitem_set.all()
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Item quantity updated in your cart.")
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        messages.success(request, "Item added to your cart.")

    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


def readallProduct(request):
    if request.method == "POST":
        if str(request.POST.get("tokens")) == "maryam80":
            user_st = UserAuth().StateLogin(request)
            if user_st["State"]:
                search = request.POST.get("search")
                listData = Product.objects.filter(user_id=user_st["User"].id).all()
                if search != "":
                    listData = Product.objects.filter(product_id=user_st["User"].id, title__contains=search).all()
                myserData = serializers.serialize("json", listData)
                return HttpResponse(myserData)
    return HttpResponse("403")

class UserAuth:
    def StateLogin(self, request):
        if request.user.is_authenticated:
            return {"State": True, "User": request.user}
        else:
            return {"State": False, "User": None}

def panel(request):
    user_st = UserAuth().StateLogin(request)
    if user_st["State"]:
        listmycart = CartItem.objects.filter(cart__user=user_st["User"]).all()
        cart_item_count = listmycart.count()
        form = productForm()
        return render(request, template_name="panel.html", context={"user_st": user_st, "listmyask": listmycart, "form": form, "cart_item_count": cart_item_count})
    else:
        return HttpResponse("Error:403, Page not available")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('view_cart')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def payment(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                charge = stripe.Charge.create(
                    amount=int(total_amount * 100),  # amount in cents
                    currency='usd',
                    description='Payment for Cart',
                    source=form.cleaned_data['stripe_token']
                )
                Payment.objects.create(
                    user=request.user,
                    amount=total_amount,
                    charge_id=charge.id
                )
                cart_items.delete()  # Clear the cart after successful payment
                messages.success(request, 'Payment successful!')
                return redirect('shop')
            except stripe.error.StripeError:
                messages.error(request, 'There was an error processing your payment. Please try again.')

    else:
        form = PaymentForm()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'form': form,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payment.html', context)
