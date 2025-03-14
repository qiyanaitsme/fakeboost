from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order

CustomUser = get_user_model()

def home_view(request):
    return render(request, "home.html")

def custom_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not email or not password1 or not password2:
            messages.error(request, "Заполните все поля.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
            return redirect("register")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким логином уже существует.")
            return redirect("register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Эта почта уже используется.")
            return redirect("register")

        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Регистрация успешна! Теперь войдите в систему.")
        return redirect("login")

    return render(request, "registration.html")


def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("user_dashboard")
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, "login.html")


@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect("/")

    users = CustomUser.objects.all()
    return render(request, "admin_panel.html", {"users": users})


@login_required
def dashboard(request):
    if request.user.is_superuser:
        users = CustomUser.objects.all()
        return render(request, "admin_panel.html", {"users": users})
    
    orders = Order.objects.filter(user=request.user)
    return render(request, "user_dashboard.html", {"user": request.user, "orders": orders})


@login_required
def boost(request):
    if request.method == "POST":
        service = request.POST.get("service")
        link = request.POST.get("link")
        boost_type = request.POST.get("boost_type")
        amount = int(request.POST.get("amount", 0))

        prices = {
            "tiktok": {"views": 0.1, "likes": 0.15, "followers": 0.2},
            "instagram": {"views": 0.13, "likes": 0.12, "followers": 0.25},
            "youtube": {"views": 0.14, "likes": 0.18, "followers": 0.3},
        }

        price_per_1000 = prices[service][boost_type] * 1000
        total_price = round((price_per_1000 * amount) / 1000, 2)

        user = User.objects.select_for_update().get(id=request.user.id)

        if user.balance < total_price:
            messages.error(request, "Недостаточно баллов!")
            return redirect("user_dashboard")

        with transaction.atomic():
            user.balance -= total_price
            user.save()

            order = Order.objects.create(
                user=user,
                service=service,
                link=link,
                boost_type=boost_type,
                amount=amount,
                price=total_price,
                progress=0,
            )

        messages.success(request, f"Заказ на {amount} {boost_type} в {service} создан!")
        return redirect("user_dashboard")

    return redirect("user_dashboard")


@login_required
def boost(request):
    if request.method == "POST":
        service = request.POST.get("service")
        link = request.POST.get("link")
        boost_type = request.POST.get("boost_type")
        amount = int(request.POST.get("amount", 0))

        prices = {
            "tiktok": {"views": 0.1, "likes": 0.15, "followers": 0.2},
            "instagram": {"views": 0.13, "likes": 0.12, "followers": 0.25},
            "youtube": {"views": 0.14, "likes": 0.18, "followers": 0.3},
        }

        price_per_1000 = prices[service][boost_type] * 1000
        total_price = round((price_per_1000 * amount) / 1000, 2)

        if request.user.balance < total_price:
            messages.error(request, "Недостаточно баллов!")
            return redirect("user_dashboard")

        request.user.balance -= total_price
        request.user.save()

        order = Order.objects.create(
            user=request.user,
            service=service,
            link=link,
            boost_type=boost_type,
            amount=amount,
            price=total_price,
            progress=0,
        )
        order.save()

        messages.success(request, f"Заказ на {amount} {boost_type} в {service} создан!")
        return redirect("user_dashboard")

    return redirect("user_dashboard")


@login_required
def dashboard(request):
    if request.user.is_superuser:
        users = CustomUser.objects.all()
        return render(request, "admin_panel.html", {"users": users})
    
    orders = Order.objects.filter(user=request.user)
    return render(request, "user_dashboard.html", {"user": request.user, "orders": orders})


@csrf_exempt
def boost_view(request):
    if request.method == "POST":
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)