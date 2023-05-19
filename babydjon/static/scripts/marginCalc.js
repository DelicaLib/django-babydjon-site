/* -----------------------------------------------margin calculator------------------------------------------------------------ */

let paddLeft = getComputedStyle(document.querySelector("main")).paddingLeft.slice(0, -1).slice(0, -1) - 20
document.querySelector("main").style.paddingLeft = paddLeft + "px"

let paddRight = getComputedStyle(document.querySelector("main")).paddingRight.slice(0, -1).slice(0, -1) - 20
document.querySelector("main").style.paddingRight = paddRight + "px"