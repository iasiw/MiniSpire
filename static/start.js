const userId = getOrCreateUserId();
function getOrCreateUserId() {
    let userId = localStorage.getItem("userId");
    if(userId == null){
        window.location.href = "/login";
    }
}


const bt1=document.getElementById("start_game");
function start_game() {
    location.href = "/login";
    }
bt1.addEventListener("click", start_game);
