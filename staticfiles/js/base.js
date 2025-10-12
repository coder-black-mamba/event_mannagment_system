const navbarDefault=document.getElementById("navbar-default")
const navbarBtn=document.getElementById("navbar-btn")

console.log("Hello From Base");

navbarBtn.addEventListener("click",()=>{
    navbarDefault.classList.toggle("hidden")
})