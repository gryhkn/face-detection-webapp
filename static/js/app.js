const history = document.getElementById("history")
const hidden = document.getElementById("hidden")

history.onclick = function (){
    if (hidden.style.display !== "none"){
        hidden.style.display = "none"
    }
    else{
        hidden.style.display = "block"
    }
}

