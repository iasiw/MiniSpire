const userId = localStorage.getItem("userId");


document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("login-form");
    const defaultUserName = document.getElementById("username");
    defaultUserName.value = userId;
    loginForm.addEventListener("submit", async function(e) {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const errorMessage = document.getElementById("error-message");
        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({username, password}),
            });
            if (!response.ok) {
                throw new Error("登录失败");
            }
            const data = await response.json();
            if (data.success) {
                localStorage.setItem("userId", username);
                const message = data.message;
                const msg = document.createElement('div');
                msg.textContent = message;
                msg.style.cssText = 'position:fixed;top:50%;right:50%;transform:translate(50%,50%);background:#a0d6a0;color:white;padding:10px;border-radius:4px;';
                document.body.appendChild(msg);
                // 3秒后自动消失
                setTimeout(() => {
                    msg.remove();
                }, 1000);
                // 登录成功，跳转到主页
                setTimeout(() => {
                    window.location.href = "/get_card?user_id="+username;
                }, 1000);
            } else {
                errorMessage.textContent = data.message;
                errorMessage.style.display = "block";
            }
        } catch (error) {
            errorMessage.textContent = "登录失败，请重试";
            errorMessage.style.display = "block";
        }
    });
});
