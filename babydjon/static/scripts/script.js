/* -----------------------------------------------background------------------------------------------------------------ */

// VANTA.TOPOLOGY({
//     el: "body",
//     mouseControls: true,
//     touchControls: true,
//     gyroControls: false,
//     minHeight: 200.00,
//     minWidth: 200.00,
//     scale: 1.00,
//     scaleMobile: 1.00,
//     color: 0x90d0b5,
//     backgroundColor: 0xd5d5d5
// })


/* -----------------------------------------------button "контакты" listener------------------------------------------------------------ */

let contactsButton = document.getElementById("contacts")
contactsButton.onclick = function() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth"
    })
}


/* -----------------------------------------------scroll------------------------------------------------------------ */

window.addEventListener("scroll", function() {
    if (window.pageYOffset > 230) {
        document.querySelector(".main-up").style.display = "block"
        document.querySelector(".main-up-arrow").style.display = "block"
    } else {
        document.querySelector(".main-up").style.display = "none"
        document.querySelector(".main-up-arrow").style.display = "none"
    }
})

document.querySelector(".main-up-arrow").addEventListener("click", function(item) {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    })
})

/* -----------------------------------------------promoution-slider------------------------------------------------------------ */
let promoutionSliderOffset = 0
const promoutionSliderLine = document.querySelector(".promoution-slider .slider-line")
let promoutionCurrentSlideId = 0
function promoutionSliderNext() {
    const slides = $(".promoution-slider .slider-line img")
    if (slides.length != 0) {
        const promoutionSlideWidth = slides[0].offsetWidth
        promoutionSliderOffset += promoutionSlideWidth
        $(".promoution-slider #" + promoutionCurrentSlideId)[0].className = "point"
        promoutionCurrentSlideId++
        if (promoutionSliderOffset >= slides.length * promoutionSlideWidth) {
            promoutionSliderOffset = 0
            promoutionCurrentSlideId = 0
        }
        $(".promoution-slider #" + promoutionCurrentSlideId)[0].className = "point point-current"
        promoutionSliderLine.style.left = -promoutionSliderOffset + "px"
    }
}
function promoutionSliderPrev() {
    const slides = $(".promoution-slider .slider-line img")
    if (slides.length != 0) {
        const promoutionSlideWidth = slides[0].offsetWidth
        promoutionSliderOffset -= promoutionSlideWidth
        $(".promoution-slider #" + promoutionCurrentSlideId)[0].className = "point"
        promoutionCurrentSlideId--
        if (promoutionSliderOffset < 0) {
            promoutionSliderOffset = (slides.length - 1) * promoutionSlideWidth
            promoutionCurrentSlideId = slides.length - 1
        }
        $(".promoution-slider #" + promoutionCurrentSlideId)[0].className = "point point-current"
        promoutionSliderLine.style.left = -promoutionSliderOffset + "px"
    }
}

function promoutinoSlideMoveTo(number) {
    const slides = $(".promoution-slider .slider-line img")
    if (slides.length != 0) {
        const promoutionSlideWidth = slides[0].offsetWidth
        promoutionSliderOffset = promoutionSlideWidth * number
        promoutionSliderLine.style.left = -promoutionSliderOffset + "px"
        $(".promoution-slider #" + promoutionCurrentSlideId)[0].className = "point"
        promoutionCurrentSlideId = number
        $(".promoution-slider #" + promoutionCurrentSlideId)[0].className = "point point-current"
    }
}


/* -----------------------------------------------random-sliders------------------------------------------------------------ */
let randomSliderLines = $(".random-slider .slider-line")
let randomSliderOffset = Array(randomSliderLines.length).fill(0)

function randomSliderNext(id) {
    const slides = $(".random-slider#" + id + " .slide")
    if (slides.length != 0) {
        const randomSlideWidth = slides.first().outerWidth(true)
        randomSliderOffset[id] += randomSlideWidth * 2
        $(".random-slider#" + id + " .slider-prev").css("display", "inline-block")
        if (randomSliderOffset[id] >= (slides.length - 6) * randomSlideWidth) {
            randomSliderOffset[id] = randomSlideWidth * 5
            $(".random-slider#" + id + " .slider-next").css("display", "none")
        }
        randomSliderLines[id].style.left = -randomSliderOffset[id] + "px"
    }
}

function randomSliderPrev(id) {
    const slides = $(".random-slider#" + id + " .slide")
    if (slides.length != 0) {
        const randomSlideWidth = slides.first().outerWidth(true)
        randomSliderOffset[id] -= randomSlideWidth * 2
        $(".random-slider#" + id + " .slider-next").css("display", "inline-block")
        if (randomSliderOffset[id] <= 0) {
            randomSliderOffset[id] = 0
            $(".random-slider#" + id + " .slider-prev").css("display", "none")
        }
        randomSliderLines[id].style.left = -randomSliderOffset[id] + "px"
    }
}


/* -----------------------------------------------modal categories------------------------------------------------------------ */
$(".modal-subcategories").css("height", $(".modal-categories").css("height"))
currentModalLink = $(".modal-link")[0]
function setCurrentModalLink() {
    currentModalLink.style.backgroundColor = "rgb(144, 208, 181)"
    currentModalLink.style.border = "2px solid black"
    currentModalLink.style.borderRight = "none"
    currentModalLink.style.borderRadius = "20px 0px 0px 20px"
    $(".modal-subcategory#"+currentModalLink.id).css("display", "flex")
}

function unsetCurrentModalLink() {
    currentModalLink.style.backgroundColor = "inherit"
    currentModalLink.style.border = "none"
    currentModalLink.style.borderRadius = "0"
    $(".modal-subcategory#"+currentModalLink.id).css("display", "none")
}
setCurrentModalLink()

$(".modal-link").mouseover(function () { 
    unsetCurrentModalLink()
    currentModalLink = this
    setCurrentModalLink()
});


function showModalCatalog() {
    let modalDiv = $(".modal.category-modal")
    let modalMain = $(".modal-main")
    modalDiv.css("display", "flex")
    let startTime = Date.now()
    const animationDurationMS = 200
    let modalTimer = setInterval(function() {
        let timePassed = Date.now() - startTime;
    
        if (timePassed > animationDurationMS) {
            modalMain.css("bottom", 0 + "%")
            clearInterval(modalTimer); // закончить анимацию через 2 секунды
            return;
        }
        let top = 100 - Math.round((timePassed / animationDurationMS) * 100)
        modalMain.css("bottom", top + "%")
    }, 20)
}

function closeModalCatalog() {
    let startTime = Date.now()
    let modalMain = $(".modal-main")
    let modalDiv = $(".modal.category-modal")
    const animationDurationMS = 200
    let modalTimer = setInterval(function() {
        let timePassed = Date.now() - startTime;
    
        if (timePassed > animationDurationMS) {
            modalMain.css("bottom", (100) + "%")
            modalDiv.css("display", "none")
            clearInterval(modalTimer); // закончить анимацию через 2 секунды
            return;
        }
        let top = Math.round((timePassed / animationDurationMS) * 100)
        modalMain.css("bottom", top + "%")
    }, 20)
}



/* -----------------------------------------------settings------------------------------------------------------------ */

function settingsCall() {
    $(".modal.profile-modal").css("display", "block");
    $(".settings-profile").addClass('active');

}

function settingsClose() {
    $(".modal.profile-modal").css("display", "none");
    $(".settings-profile.active").removeClass('active');
}

/* -----------------------------------------------deliveryAddressValidation------------------------------------------------------------ */