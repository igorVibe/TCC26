// ========================================
// CONFIGURAÇÕES
// ========================================

const API_URL = "http://127.0.0.1:8000";


// ========================================
// ELEMENTOS DA PÁGINA
// ========================================

const roversContainer =
    document.getElementById("roversContainer");

const refreshButton =
    document.getElementById("refreshButton");

const logoutButton =
    document.getElementById("logoutButton");


// ========================================
// CARREGAR ROVERS
// ========================================

async function carregarRovers() {

    try {

        // Pega o token atual
        const token =
            localStorage.getItem("access_token");


        console.log(
            "🔐 Token encontrado:",
            token ? "SIM" : "NÃO"
        );


        // ========================================
        // VERIFICAR TOKEN
        // ========================================

        if (!token) {

            console.error(
                "❌ Nenhum token encontrado."
            );

            window.location.href =
                "login.html";

            return;

        }


        // ========================================
        // MENSAGEM DE CARREGAMENTO
        // ========================================

        roversContainer.innerHTML = `
            <div class="loading">
                Carregando rovers...
            </div>
        `;


        // ========================================
        // REQUISIÇÃO PARA A API
        // ========================================

        const response = await fetch(
            `${API_URL}/rovers/`,
            {

                method: "GET",

                headers: {

                    "Authorization":
                        `Bearer ${token}`,

                    "Content-Type":
                        "application/json"

                }

            }
        );


        console.log(
            "📡 Status da API:",
            response.status
        );


        // ========================================
        // TOKEN INVÁLIDO
        // ========================================

        if (response.status === 401) {

            console.error(
                "❌ Token inválido ou expirado."
            );


            localStorage.removeItem(
                "access_token"
            );

            localStorage.removeItem(
                "refresh_token"
            );


            window.location.href =
                "login.html";


            return;

        }


        // ========================================
        // OUTRO ERRO
        // ========================================

        if (!response.ok) {

            throw new Error(
                `Erro HTTP ${response.status}`
            );

        }


        // ========================================
        // CONVERTER RESPOSTA
        // ========================================

        const resultado =
            await response.json();


        console.log(
            "🤖 Rovers recebidos:",
            resultado
        );


        // ========================================
        // TRATAR PAGINAÇÃO
        // ========================================

        const rovers =
            resultado.results || resultado;


        // ========================================
        // VERIFICAR ROVERS
        // ========================================

        if (
            !rovers ||
            rovers.length === 0
        ) {

            roversContainer.innerHTML = `
                <div class="loading">
                    Nenhum Rover cadastrado.
                </div>
            `;

            return;

        }


        // ========================================
        // LIMPAR CONTAINER
        // ========================================

        roversContainer.innerHTML = "";


        // ========================================
        // CRIAR CARDS
        // ========================================

        rovers.forEach(
            rover => {

                const card =
                    document.createElement("div");


                card.className =
                    "rover-card";


                // ========================================
                // STATUS
                // ========================================

                let status = "Offline";
                let statusClass = "offline";


                if (
                    rover.ultima_conexao
                ) {

                    status = "Online";
                    statusClass = "online";

                }


                // ========================================
                // CARD
                // ========================================

                card.innerHTML = `

                    <div class="rover-card-header">

                        <div>

                            <h3>
                                ${rover.nome}
                            </h3>

                            <small>
                                ${rover.id_rover}
                            </small>

                        </div>


                        <span
                            class="rover-status ${statusClass}"
                        >

                            ${status === "Online"
                                ? "🟢"
                                : "🔴"
                            }

                            ${status}

                        </span>

                    </div>


                    <div class="rover-info">


                        <div
                            class="rover-info-item"
                        >

                            <span>
                                🤖 ID
                            </span>

                            <strong>
                                ${rover.id_rover}
                            </strong>

                        </div>


                        <div
                            class="rover-info-item"
                        >

                            <span>
                                🔋 Bateria
                            </span>

                            <strong>
                                ${rover.bateria ?? "--"}%
                            </strong>

                        </div>


                        <div
                            class="rover-info-item"
                        >

                            <span>
                                🕐 Última conexão
                            </span>

                            <strong>
                                ${formatarData(
                                    rover.ultima_conexao
                                )}
                            </strong>

                        </div>


                    </div>

                `;


                roversContainer.appendChild(
                    card
                );

            }
        );


        console.log(
            "✅ Rovers carregados com sucesso!"
        );


    } catch (error) {

        console.error(
            "❌ Erro ao carregar Rovers:",
            error
        );


        roversContainer.innerHTML = `
            <div class="loading">

                ❌ Não foi possível
                conectar à API.

            </div>
        `;

    }

}


// ========================================
// FORMATAR DATA
// ========================================

function formatarData(data) {

    if (!data) {

        return "--";

    }


    const dataFormatada =
        new Date(data);


    return dataFormatada.toLocaleString(
        "pt-BR"
    );

}


// ========================================
// BOTÃO ATUALIZAR
// ========================================

if (refreshButton) {

    refreshButton.addEventListener(
        "click",
        carregarRovers
    );

}


// ========================================
// LOGOUT
// ========================================

if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        () => {

            localStorage.removeItem(
                "access_token"
            );

            localStorage.removeItem(
                "refresh_token"
            );

            window.location.href =
                "login.html";

        }
    );

}


// ========================================
// INICIAR
// ========================================

carregarRovers();