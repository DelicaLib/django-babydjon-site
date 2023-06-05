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
    productContext["product"] = myDatabase.getProductData(productId=productid)
    productContext["sizes"] = myDatabase.getSizes(productContext["product"])
    return render(request, "shop/product.html", productContext)



def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")



def profile(request):
    if "is_login" not in request.session or not request.session["is_login"]:
        request.session["loginContext"] = "Профиль"
        return HttpResponseRedirect("/login/")
    if "signout" in request.POST:
        del request.session["is_login"]
        del request.session["userId"]
        return HttpResponseRedirect("/login/")
    if "settings" in request.POST:
        result = myDatabase.setUserSettings(request.session["userId"], request.POST["fullName"], request.POST["email"], request.POST["phone"], request.POST["address"], request.POST["password"], request.POST["newPassword"], request.POST["newPasswordRepeat"])
        if result != "0":
            request.session["errorSetting"] = result
            request.session["is_settings"] = True
            return HttpResponseRedirect("/profile/")
        else:
            if "is_settings" in request.session:
                del request.session["is_settings"]
            return HttpResponseRedirect("/profile/")
    context = profileContext.copy()
    context["user"] = myDatabase.getUserData(request.session["userId"])
    if "createCard" in request.POST:
        myDatabase.createBonusCard(context["user"].Id)
        return HttpResponseRedirect("/profile/")
    return render(request, "shop/profile.html", context)



def cart(request):
    if "is_login" not in request.session or not request.session["is_login"]:
        request.session["loginContext"] = "Корзина"
        return HttpResponseRedirect("/login/")
    context = cartContext.copy()
    context["cart"] = myDatabase.getCartData(request.session["userId"])
    if len(context["cart"]["data"]) == 0:
        context["cart"]["data"] = None
    return render(request, "shop/cart.html", context)



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
    context = profileContext.copy()
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
    context = profileContext.copy()
    context["currPage"] = request.session["loginContext"]
    del request.session["loginContext"]
    return render(request, "shop/registration.html", context)