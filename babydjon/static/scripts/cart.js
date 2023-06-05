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