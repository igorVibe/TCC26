const API_URL = "http://127.0.0.1:8000";

const loginForm = document.getElementById("loginForm");
const loginMessage = document.getElementById("loginMessage");


loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    loginMessage.textContent = "Entrando...";
    loginMessage.style.color = "#6b7280";

    try {

        const response = await fetch(`${API_URL}/api/token/`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                password: password
            })

        });


        const data = await response.json();


        if (!response.ok) {

            loginMessage.textContent =
                "Usuário ou senha inválidos.";

            loginMessage.style.color = "#dc2626";

            return;
        }


        // Salva os tokens
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);


        loginMessage.textContent =
            "Login realizado com sucesso!";

        loginMessage.style.color = "#16a34a";


        // Vai para o Dashboard
        setTimeout(() => {

            window.location.href = "index.html";

        }, 500);


    } catch (error) {

        console.error(error);

        loginMessage.textContent =
            "Não foi possível conectar à API.";

        loginMessage.style.color = "#dc2626";

    }

});