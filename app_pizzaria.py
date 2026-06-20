import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Pizza Control",
    layout="wide"
)

# LOGIN

USUARIO="gilvan"
SENHA="gilvan2008"

if "logado" not in st.session_state:
    st.session_state.logado=False

if "pedidos" not in st.session_state:
    st.session_state.pedidos=[]

if not st.session_state.logado:

    c1,c2,c3=st.columns([1,1,1])

    with c2:

        st.title("🍕 Pizza Control")

        usuario=st.text_input(
            "Usuário"
        )

        senha=st.text_input(
            "Senha",
            type="password"
        )

        if st.button(
            "Entrar",
            use_container_width=True
        ):

            if (
                usuario==USUARIO
                and
                senha==SENHA
            ):

                st.session_state.logado=True
                st.rerun()

            else:

                st.error(
                    "Login inválido"
                )

    st.stop()

menu=st.sidebar.radio(
    "MENU",
    [
        "🍕 NOVO PEDIDO",
        "👨‍🍳 COZINHA",
        "📊 DASHBOARD"
    ]
)

sabores=[

"NAPOLITANA",
"CAMARÃO",
"CAIPIRA",
"MINEIRA",
"MODA DA CASA",
"STROGONOFF",
"CALABRESA",
"PORTUGUESA",
"FRANGO CATUPIRY",
"4 QUEIJOS",
"MEXICANA"

]

# PEDIDOS

if menu=="🍕 NOVO PEDIDO":

    st.title("Novo Pedido")

    c1,c2=st.columns(2)

    mesa=c1.selectbox(
        "Mesa",
        range(1,31)
    )

    pizza=c2.selectbox(
        "Pizza",
        sabores
    )

    if st.button(
        "Enviar para Cozinha"
    ):

        st.session_state.pedidos.append({

            "hora":
            datetime.now(),

            "mesa":
            mesa,

            "pizza":
            pizza,

            "status":
            "PREPARANDO"

        })

        st.success(
            "Pedido enviado"
        )

# COZINHA

elif menu=="👨‍🍳 COZINHA":

    st.title(
        "Painel Cozinha"
    )

    preparando=[]
    prontos=[]

    for i,p in enumerate(
        st.session_state.pedidos
    ):

        if p["status"]=="PREPARANDO":

            preparando.append(
                (i,p)
            )

        else:

            prontos.append(
                (i,p)
            )

    col1,col2=st.columns(2)

    with col1:

        st.subheader(
            "🔥 PREPARANDO"
        )

        for i,p in preparando:

            st.info(
f"""
🪑 Mesa {p["mesa"]}

🍕 {p["pizza"]}

🕒 {p["hora"].strftime("%H:%M")}
"""
            )

            if st.button(
                f"FINALIZAR {i}"
            ):

                st.session_state.pedidos[i][
                    "status"
                ]="PRONTO"

                st.rerun()

    with col2:

        st.subheader(
            "✅ PRONTOS"
        )

        for i,p in prontos:

            st.success(
f"""
Mesa {p["mesa"]}

🍕 {p["pizza"]}
"""
            )

# DASHBOARD

elif menu=="📊 DASHBOARD":

    st.title(
        "Dashboard"
    )

    if len(
        st.session_state.pedidos
    )>0:

        df=pd.DataFrame(
            st.session_state.pedidos
        )

        m1,m2,m3=st.columns(3)

        m1.metric(
            "Pedidos",
            len(df)
        )

        m2.metric(
            "Prontos",

            (
                df["status"]
                ==
                "PRONTO"
            ).sum()
        )

        hora=(
            df["hora"]
            .dt.hour
            .mode()[0]
        )

        m3.metric(
            "Hora Pico",
            f"{hora}:00"
        )

        st.subheader(
            "🍕 Mais Pedidas"
        )

        top=(

            df

            .groupby(
                "pizza"
            )

            .size()

            .reset_index(
                name="pedidos"
            )

        )

        grafico=px.bar(

            top,

            x="pizza",

            y="pedidos"

        )

        st.plotly_chart(
            grafico,
            use_container_width=True
        )

        st.subheader(
            "Histórico"
        )

        st.dataframe(
            df
        )

    else:

        st.info(
            "Sem pedidos"
        )

if st.sidebar.button(
    "Sair"
):

    st.session_state.logado=False

    st.rerun()
