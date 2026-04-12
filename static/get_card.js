//生成用户ID
const userId = getOrCreateUserId();
function getOrCreateUserId() {
    let userId = localStorage.getItem("userId");
    if(userId == null){
        window.location.href = "/login";
    }
    return userId;
}
//全局变量
let ready_to_play = 0
// 加载页面时获取用户数据
document.addEventListener("DOMContentLoaded",async function() {
    const response = await fetch("/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({user_id: userId}),
        cache: "no-cache",
    });
    if (!response.ok) {
        throw new Error("Network response was not ok");
    }
    const data = await response.json();
    const exists = data[0].exists;
    if(!exists){
        alert("用户信息异常,即将跳转至登录页面");
        window.location.href = "/login";
    }
    const count_ku = data[0].count_ku;
    if (count_ku == 10) {
        ready_to_play = 1;
    }
    else {
        ready_to_play = 0;
    }
    const count_ku_element = document.getElementById("count_ku");
    count_ku_element.textContent = count_ku;
    const count_library_element = data[0].count_library;

    for (let i = 0; i < count_ku; i++) {
        const selected_cards_list = document.getElementById("selected-cards-list");
        const new_card_item = document.createElement("div");
        new_card_item.className = "card_selected";
        new_card_item.setAttribute("selected-card-id", i+1);
        new_card_item.innerHTML = `
            <div class="card-name">${data[0].player_cards[i].name}</div>
            <div class="card-cost">${data[0].player_card_type[i]}</div>
            <div class="card-desc">${data[0].player_cards[i].description}</div>
        `;
        selected_cards_list.appendChild(new_card_item);
    }

    for (let i = 0; i < count_library_element; i++) {
        const library_cards_list = document.getElementById("card-grid");
        const new_card_item = document.createElement("div");
        new_card_item.className = "card";
        new_card_item.setAttribute("data-card-id", i+1);
        new_card_item.innerHTML = `
            <div class="card-name">${data[0].library_card_name[i+1]}</div>
            <div class="card-cost">${data[0].library_card_type[i+1]}</div>
            <div class="card-desc">${data[0].library_card_desc[i+1]}</div>
        `;
        library_cards_list.appendChild(new_card_item);
    }

// 点击卡牌
document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("click",async function() {
        const card_id = this.getAttribute("data-card-id");
        const response = await fetch("/get_card", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({card_id: card_id,user_id: userId}),
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        const message = data.message;
        const print = data.print;
        //if (print == 1) {
            //alert(message);
        //}
        const msg = document.createElement('div');
        msg.textContent = message;
        msg.style.cssText = 'position:fixed;top:50%;right:50%;transform:translate(50%,50%);background:#a0d6a0;color:white;padding:10px;border-radius:4px;';
        document.body.appendChild(msg);
        // 3秒后自动消失
        setTimeout(() => {
            msg.remove();
        }, 500);
        setTimeout(() => {
            location.reload();
        }, 500);
    });
});
// 开始游戏按钮
    const start_game_button = document.getElementById("start-game-btn");
    start_game_button.addEventListener("click",async function() {
        if (ready_to_play == 1) {
            location.href = "/play?user_id="+userId;
        }
        else {
            const msg = document.createElement('div');
            msg.textContent = "请先添加足够数量的卡牌";
            msg.style.cssText = 'position:fixed;top:50%;right:50%;transform:translate(50%,50%);background:#a0d6a0;color:white;padding:10px;border-radius:4px;';
            document.body.appendChild(msg);
            setTimeout(() => {
                msg.remove();
            }, 500);
            }
    });
// 重置游戏按钮
    const reset_game_button = document.getElementById("reset-game-btn");
    reset_game_button.addEventListener("click",async function() {
        const response = await fetch("/reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({user_id: userId}),
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        const message = data.message;
        const msg = document.createElement('div');
        msg.textContent = message;
        msg.style.cssText = 'position:fixed;top:50%;right:50%;transform:translate(50%,50%);background:#a0d6a0;color:white;padding:10px;border-radius:4px;';
        document.body.appendChild(msg);
        setTimeout(() => {
            msg.remove();
        }, 500);
        setTimeout(() => {
            location.reload();
        }, 500);
    });
// 保存卡组按钮
    const save_button = document.getElementById("save-btn");
    save_button.addEventListener("click",async function() {
        const response = await fetch("/save_cards", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({user_id: userId}),
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        const message = data.message;
        const msg = document.createElement('div');
        msg.textContent = message;
        msg.style.cssText = 'position:fixed;top:50%;right:50%;transform:translate(50%,50%);background:#a0d6a0;color:white;padding:10px;border-radius:4px;';
        document.body.appendChild(msg);
        setTimeout(() => {
            msg.remove();
        }, 500);
        setTimeout(() => {
            location.reload();
        }, 500);
    });
// 加载卡组按钮
    const load_button = document.getElementById("load-btn");
    load_button.addEventListener("click",async function() {
        const response = await fetch("/load_cards", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({user_id: userId}),
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        const message = data.message;
        const msg = document.createElement('div');
        msg.textContent = message;
        msg.style.cssText = 'position:fixed;top:50%;right:50%;transform:translate(50%,50%);background:#a0d6a0;color:white;padding:10px;border-radius:4px;';
        document.body.appendChild(msg);
        setTimeout(() => {
            msg.remove();
        }, 500);
        setTimeout(() => {
            location.reload();
        }, 500);
    });
});
