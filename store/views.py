import stripe
from django.conf import settings
from django.urls import reverse
from django.http import HttpRequest, HttpResponse


def checkout(request: HttpRequest) -> HttpResponse:
    """Stripe checkout: create session and redirect."""
    cart = request.session.get("cart", {})
    products = Product.objects.filter(pk__in=cart.keys())
    line_items = []
    for product in products:
        quantity = cart[str(product.pk)]
        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": int(product.price * 100),
                },
                "quantity": quantity,
            }
        )
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("store:cart_view"))
        + "?success=true",
        cancel_url=request.build_absolute_uri(reverse("store:cart_view")),
    )
    return redirect(session.url)


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product
from .forms import UserRegisterForm


def register(request: HttpRequest) -> HttpResponse:
    """User registration view."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("store:home")
    else:
        form = UserRegisterForm()
    return render(request, "store/register.html", {"form": form})


def user_login(request: HttpRequest) -> HttpResponse:
    """User login view."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("store:home")
        else:
            messages.error(request, "Invalid username or password.")
    from django.contrib.auth.forms import AuthenticationForm

    form = AuthenticationForm()
    return render(request, "store/login.html", {"form": form})


def user_logout(request: HttpRequest) -> HttpResponse:
    """User logout view."""
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("store:home")


def cart_view(request: HttpRequest) -> HttpResponse:
    """Display the shopping cart."""
    cart = request.session.get("cart", {})
    products = Product.objects.filter(pk__in=cart.keys())
    cart_items = []
    for product in products:
        quantity = cart[str(product.pk)]
        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "total": product.price * quantity,
            }
        )
    total_price = sum(item["total"] for item in cart_items)
    return render(
        request,
        "store/cart.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


def add_to_cart(request: HttpRequest, pk: int) -> HttpResponse:
    """Add a product to the cart."""
    cart = request.session.get("cart", {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session["cart"] = cart
    return redirect("store:cart_view")


def remove_from_cart(request: HttpRequest, pk: int) -> HttpResponse:
    """Remove a product from the cart."""
    cart = request.session.get("cart", {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session["cart"] = cart
    return redirect("store:cart_view")


from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Product


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Product detail page."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


def products_list(request: HttpRequest) -> HttpResponse:
    """Products page: lists all products."""
    products = Product.objects.all()
    return render(request, "store/products.html", {"products": products})


def home(request: HttpRequest) -> HttpResponse:
    """Landing page for the store."""
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})
