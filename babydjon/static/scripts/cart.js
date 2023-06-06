/---------------------------------------------select-------------------------------------------------/
function optionChange(self){
    if (self.value == "courier" || self.value == "urgentCourier" || self.value == "mail") {
        $(".delivery-address").css("display", "flex")
    }
    else {
        $(".delivery-address").css("display", "none")
    }
    if (self.value == "self-delivery") {
        $("#for-offline-map").css("display", "block")
        $(".offline-addresses").css("display", "flex")
    }
    else {
        $("#for-offline-map").css("display", "none")
        $(".offline-addresses").css("display", "none")
    }
}

/-----------------------------------------------check all--------------------------------------------------------/
function checkAll() {
    if ($("#check-all").prop("checked")) {
        $("input[name='check-one'").prop("checked", true)
    }
    else {
        $("input[name='check-one'").prop("checked", false)
    }
}

/-----------------------------------------------delete checked products---------------------------------/
function deleteChecked() {
    var allChecked = []
    $("input[name='check-one']:checked").each(function() {
        allChecked.push(Number($(this).prop("id").replace("check_id", "")))
    })
    var csrf_token = $("#delete-checked input").val()
    if (allChecked.length == 0) {
        return -1
    }
    $.ajax({
        url: "/cart/deleteProductsFromCart/",
        method: "POST",
        dataType: "json",
        data: {productsId: '[' + allChecked + ']', csrfmiddlewaretoken: csrf_token},
        success: function(response) {
            console.log(response.status, "Удалено " + response.deleted + " товаров из корзины")
            allChecked.forEach(i => {
                $("#product_id"+i).remove()
            });
            if ($(".cart-main-product").length == 0) {
                location.reload()
            }
        },
        error: function(response) {
            console.log(response.responseJSON.errors)
        }

    })
    console.log(allChecked)
}

function deleteOne(productId) {
    var csrf_token = $("#delete_id"+productId+" input").val()
    $.ajax({
        url: "/cart/deleteOneProductFromCart/",
        method: "POST",
        dataType: "json",
        data: {productId: Number(productId), csrfmiddlewaretoken: csrf_token},
        success: function(response) {
            console.log(response.status, "Удалено")
            $("#product_id"+productId).remove()
            if ($(".cart-main-product").length == 0) {
                location.reload()
            }
        },
        error: function(response) {
            console.log(response.responseJSON.errors)
        }

    })
}

/-------------------------------------------------------update cost-----------------------------------------------------/

function updateCost() {
    var checkedProducts = $("input[name='check-one']:checked")
    var cartProducts = []
    checkedProducts.each(function() {
        var currId = Number($(this).prop("id").replace("check_id", ""))
        cartProducts.push(currId)
    })
    bonusCard = $("input#useBonusCard").prop("checked") ? 1 : 0
    $.ajax({
        url: "/cart/updateCost/",
        method: "GET",
        dataType: "json",
        data: {cartProducts: "["+cartProducts+"]", bonusCard: bonusCard},
        success: function(response) {
            console.log(response.status)
            $(".cart-info-money p.cost span#num").text(response.cost)
            $(".cart-info-money p.bonus span#num").text(response.bonuses)
            $(".cart-info-buy p.sum span#num").text(response.sumCost)
        },
        error: function(response) {
            console.log(response.responseJSON.errors)
        }

    })

}

$("input#product-count").on("change", function() {

    count = Number($(this).val())
    if (count > Number($(this).prop("max")))
    {
        $(this).val($(this).prop("max"))
    }
    if (count < Number($(this).prop("min")))
    {
        $(this).val($(this).prop("min"))
    }
    count = Number($(this).val())
    productElement = $(this).parent().parent().parent()
    productId = productElement.prop("id").replace("product_id", "")
    $.ajax({
        url: "/cart/updateCountInCart/",
        method: "GET",
        dataType: "json",
        data: {productId: productId, count: count},
        success: function(response) {
            console.log(response.status)
            $("#product_id" + productId + " .product-cost span.cost").text(response.cost)
            updateCost()
        },
        error: function(response) {
            console.log(response.responseJSON.errors)
            location.reload()
        }

    })
})