import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Pizzaria",
    layout="wide"
)

# LOGIN
USUARIO = "gilvan"
SENHA = "gilvan2008"

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:

    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        if (
            usuario == USUARIO and
            senha == SENHA
        ):
            st.session_state.logado = True
            st.rerun()

        else:
            st.error(
                "Usuário ou senha inválidos"
            )

    st.stop()

# SISTEMA
if "pedidos" not in st.session_state:
    st.session_state.pedidos = []

sabores = [
"NAPOLITANA",
"CAMARÃO",
"MINEIRA",
"MODA DA CASA",
"STROGONOFF",
"CALABRESA",
"PORTUGUESA",
"FRANGO CATUPIRY",
"4 QUEIJOS",
"MEXICANA"
]

st.title("🍕 Sistema da Pizzaria")

col1, col2 = st.columns([1,2])

with col1:

    st.subheader("Novo Pedido")

    mesa = st.selectbox(
        "Mesa",
        [f"Mesa {i}" for i in range(1,31)]
    )

    pizza = st.selectbox(
        "Pizza",
        sabores
    )

    qtd = st.number_input(
        "Quantidade",
        min_value=1,
        value=1
    )

    if st.button("Enviar Pedido"):

        st.session_state.pedidos.append(
            {
                "Hora":
                datetime.now().strftime(
                    "%H:%M"
                ),

                "Mesa": mesa,

                "Pizza": pizza,

                "Quantidade": qtd,

                "Status":
                "Preparando"
            }
        )

        st.success(
            "Pedido enviado"
        )

with col2:

    st.subheader(
        "👨‍🍳 Cozinha"
    )

    if st.session_state.pedidos:

        total = sum(
            p["Quantidade"]
            for p in
            st.session_state.pedidos
        )

        st.metric(
            "Pedidos Pendentes",
            total
        )

        for i, pedido in enumerate(
            st.session_state.pedidos
        ):

            st.write(
f"""
🍕 {pedido["Pizza"]}

🪑 {pedido["Mesa"]}

🔢 {pedido["Quantidade"]}

🕒 {pedido["Hora"]}

📌 {pedido["Status"]}
"""
            )

            if (
                pedido["Status"]
                !=
                "Pronto"
            ):

                if st.button(
                    f"Concluir {i}"
                ):

                    st.session_state.pedidos[i][
                        "Status"
                    ] = "Pronto"

                    st.rerun()

    else:

        st.info(
            "Sem pedidos"
        )

if st.button(
    "Sair"
):

    st.session_state.logado = False

    st.rerun()
