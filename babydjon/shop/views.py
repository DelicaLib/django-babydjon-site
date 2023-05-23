from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from shop.models import Category
import shop.contexts as contexts
import shop.database as myDatabase

indexContext = contexts.indexContext()
productContext = contexts.productContext()
profileContext = contexts.profileContext()
cartContext = contexts.cartContext()
ordersContext = contexts.ordersContext()
addressesContext = contexts.addressesContext()

def index(request):
    return render(request, "shop/index.html", indexContext)

def product(request, productid):
    productContext["productId"] = productid
    return render(request, "shop/product.html", productContext)

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def profile(request):
    if "is_login" not in request.session or not request.session["is_login"]:
        request.session["loginContext"] = "Профиль"
        return HttpResponseRedirect("/login/")
    return render(request, "shop/product.html", profileContext)

def cart(request):
    if "is_login" not in request.session or not request.session["is_login"]:
        request.session["loginContext"] = "Корзина"
        return HttpResponseRedirect("/login/")
    return render(request, "shop/cart.html", cartContext)

def orders(request):
    if "is_login" not in request.session or not request.session["is_login"]:
        request.session["loginContext"] = "Заказы"
        return HttpResponseRedirect("/login/")
    return render(request, "shop/orders.html", ordersContext)

def addresses(request):
    return render(request, "shop/addresses.html", addressesContext)

def login(request):
    if "auth" in request.POST:
        login = request.POST["login"]
        password = request.POST["password"]
        userId = myDatabase.login(login=login, password=password)
        if userId == -1:
            request.session["errorLogin"] = "Неправильный логин/пароль"
        else:
            request.session["is_login"] = True
            request.session["userId"] = userId
            return HttpResponseRedirect("/profile/")
        
    if "is_login" in request.session and request.session["is_login"]:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if "loginContext" not in request.session:
        request.session["loginContext"] = "Профиль"
    context = profileContext
    context["currPage"] = request.session["loginContext"]
    del request.session["loginContext"]
    return render(request, "shop/authorization.html", context)

def registration(request):
    if "reg" in request.POST:
        firstname = request.POST["firstname"]
        secondname = request.POST["secondname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        login = request.POST["login"]
        password = request.POST["password"]
        myDatabase.register(firstname=firstname, secondname=secondname, email=email, phone=phone, login=login, password=password)
        return HttpResponseRedirect("/login/")
    if "is_login" in request.session and request.session["is_login"]:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if "loginContext" not in request.session:
        request.session["loginContext"] = "Профиль"
    context = profileContext
    context["currPage"] = request.session["loginContext"]
    del request.session["loginContext"]
    return render(request, "shop/registration.html", context)