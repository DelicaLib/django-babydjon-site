from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse, Http404
import shop.contexts as contexts
import shop.database as myDatabase
import json as json

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
    context["bonusMinus"] = myDatabase.connection.cursor().execute(f"select sum([Order].[Bonuses]) from [Order] where [Order].[Buyer] = {request.session['userId']}").fetchone()[0]
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
# ----------------------------------------------for Ajax-----------------------------------

def deleteOneProductFromCart(request):
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            deletedCount = myDatabase.deleteOneProductFromCart(request.POST["productId"], request.session["userId"])
        except:
            return JsonResponse({"errors" : "Ошибка при удалении"}, status=500)
        if deletedCount != 0:
            return JsonResponse({"status" : "OK"}, status=200)
        else:
            return JsonResponse({"errors" : "Ошибка при удалении"}, status=400)
    else:
        raise Http404()
    
def deleteProductsFromCart(request):
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            deletedCount = myDatabase.deleteProductsFromCart(request.POST["productsId"], request.session["userId"])
        except:
            return JsonResponse({"errors" : "Ошибка при удалении"}, status=500)
        if deletedCount != 0:
            return JsonResponse({"status" : "OK", "deleted" : deletedCount}, status=200)
        else:
            return JsonResponse({"errors" : "Ошибка при удалении"}, status=400)
    else:
        raise Http404()
    
def updateCost(request):
    if request.method == "GET" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        cartProducts = json.loads(request.GET["cartProducts"])
        useBonusCard = json.loads(request.GET["bonusCard"])
        if len(cartProducts) == 0:
            return JsonResponse({"status" : "OK", "cost" : 0, "bonuses" : 0, "sumCost" : 0}, status=200)
        cost = int(myDatabase.getSumCostInCart(cartProducts, request.session["userId"]))
        bonuses = 0
        sumCost = cost
        myDatabase.getBonusCardBalance(request.session["userId"])
        if useBonusCard == 0:
            bonuses = "+" + str(int(float(cost) * 0.05))
        else:
            bonuses = myDatabase.getBonusCardBalance(request.session["userId"])
            if (bonuses[0] == "-"):
                bonusesNum = abs(int(bonuses))
                if cost <= bonusesNum:
                    sumCost = 0
                    bonuses = "-" + str(cost)
                else:
                    sumCost -= bonusesNum
        
                
        return JsonResponse({"status" : "OK", "cost" : cost, "bonuses" : bonuses, "sumCost" : sumCost}, status=200)
    else:
        raise Http404()
    
def updateCountInCart(request):
    if request.method == "GET" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        productId = json.loads(request.GET["productId"])
        count = json.loads(request.GET["count"])
        updateInfo = myDatabase.updateCartCount(request.session["userId"], productId, count)
        if (updateInfo["updateCount"] == 0):
            return JsonResponse({"errors" : "Ошибка при изменении"}, status=400)
        
        return JsonResponse({"status" : "OK", "cost" : updateInfo["cost"]}, status=200)
    else:
        raise Http404()