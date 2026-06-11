const userId = getOrCreateUserId();
function getOrCreateUserId() {
    let userId = localStorage.getItem("userId");
    if(userId == null){
        window.location.href = "/login";
    }
    return userId;
}

async function connectWebSocket() {
    const response = await fetch("/getWebSocketUrl", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        cache: "no-cache",
    });
    if (!response.ok) {
        throw new Error("Network response was not ok");
    }
    const data = await response.json();
    const WEBSOCKET_URL = data.websocket_url;
    const websocket = new WebSocket(WEBSOCKET_URL+"/ws?userId="+userId);
    websocket.onopen = function() {
        console.log("已连接");
    }
    websocket.onmessage = function(event) {
        const message = event.data;
        if (message == "reload") {
            location.reload();
        }
    }
}
window.addEventListener("load", function() {
    connectWebSocket();
});
window.addEventListener("unload", function() {

    websocket.close();

});


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
    const player_health = document.getElementById("player-health-value");
    const player_health_bar = document.getElementById("player-health");
    player_health_bar.style.width = data[0].player_health + "%";
    const enemy_health = document.getElementById("enemy-health-value");
    const enemy_health_bar = document.getElementById("enemy-health");
    enemy_health_bar.style.width = data[0].enemy_health + "%";
    player_health.textContent = data[0].player_health;
    enemy_health.textContent = data[0].enemy_health;
    const player_energy = document.getElementById("player-energy");
    player_energy.textContent = data[0].player_energy;
    const enemy_energy = document.getElementById("enemy-energy");
    enemy_energy.textContent = data[0].enemy_energy;
    const player_block = document.getElementById("player-block");
    player_block.textContent = data[0].player_block;
    const enemy_block = document.getElementById("enemy-block");
    enemy_block.textContent = data[0].enemy_block;
    const player_shield = document.getElementById("player-shield");
    player_shield.textContent = data[0].player_shield;
    const enemy_shield = document.getElementById("enemy-shield");
    enemy_shield.textContent = data[0].enemy_shield;
    const message_log = document.getElementById("message-log");
    message_log.value = data[0].message_log;
    message_log.scrollTop = message_log.scrollHeight;

    for (let i = 0; i < data[0].count_hand_cards; i++) {
        const player_hand = document.getElementById("player-hand");
        const new_card_item = document.createElement("div");
        new_card_item.className = "card";
        new_card_item.setAttribute("data-card-id", i+1);
        new_card_item.innerHTML = `
            <div class="card-name">${data[0].player_hand_cards[i].name}</div>
            <div class="card-cost">${data[0].player_hand_card_type[i]}</div>
            <div class="card-desc">${data[0].player_hand_cards[i].description}</div>
        `;
        player_hand.appendChild(new_card_item);
    };
    async function repeat_play() {
        const repeat = data[0].repeat;
        if (repeat) {
             const dict = await fetch("/play",{
                method: "POST",
                headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({card_id: 0,user_id: userId}),  // 添加 card_id 参数
            });
            if (!dict.ok) {
                throw new Error("Network response was not ok");
            }
            const information = await dict.json();
            const message = information.message;
            const msg = document.createElement('div');
            msg.textContent = message;
            msg.style.cssText = 'position:fixed;top:50%;right:50%;transform:translate(50%,50%);background:#a0d6a0;color:white;padding:10px;border-radius:4px;';
            document.body.appendChild(msg);
            // 3秒后自动消失
            setTimeout(() => {
                msg.remove();
            }, 1000);
            setTimeout(() => {
                location.reload();
            }, 1000);
        }
    }
    repeat_play();

    async function post_card_id() {
        const card_id = this.getAttribute("data-card-id");
        const response = await fetch("/play", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({card_id: card_id,user_id: userId}),
            cache: "no-cache",
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
        // 3秒后自动消失
        setTimeout(() => {
            msg.remove();
        }, 600);
        setTimeout(() => {
            location.reload();
        }, 600);
    }

    const finish_round_btn = document.getElementById("end-turn-btn");
    finish_round_btn.addEventListener("click", post_card_id);

    document.querySelectorAll(".card").forEach(card => {
        card.addEventListener("click", post_card_id);
    });

    const restart_btn = document.getElementById("restart-btn");
    restart_btn.addEventListener("click",async function() {
        const response = await fetch("/reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({user_id: userId}),
            cache: "no-cache",
        });
        const data = await response.json();
        const message = data.message;
        const msg = document.createElement('div');
        msg.textContent = message;
        msg.style.cssText = 'position:fixed;top:50%;right:50%;transform:translate(50%,50%);background:#a0d6a0;color:white;padding:10px;border-radius:4px;';
        document.body.appendChild(msg);
        // 3秒后自动消失
        setTimeout(() => {
            msg.remove();
        }, 100);
        setTimeout(() => {
            location.href = "/get_card?user_id="+userId;
        }, 100);
    });

    if (data[0].player_health <= 0) {
        // 玩家失败
        showGameOverModal(false);
    }
    if (data[0].enemy_health <= 0) {
        // 玩家胜利
        showGameOverModal(true);
    }


});
function showGameOverModal(isVictory) {
    const gameOverModal = document.getElementById("game-over-modal");
    const gameResult = document.getElementById("game-result");
    const gameMessage = document.getElementById("game-message");

    if (isVictory) {
        gameResult.textContent = "胜利！";
        gameMessage.textContent = "你成功击败了敌人！";
    } else {
        gameResult.textContent = "失败！";
        gameMessage.textContent = "你被敌人击败了！";
    }

    // 显示模态框
    gameOverModal.classList.remove("hidden");
}