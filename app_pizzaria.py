import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Pizza Control",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
background:#0f1117;
color:white;
}

.card{
background:#181c25;
padding:20px;
border-radius:18px;
margin-bottom:10px;
}

.block-container{
padding-top:1rem;
}

</style>
""",unsafe_allow_html=True)

USUARIO="gilvan"
SENHA="gilvan2008"

if "login" not in st.session_state:
    st.session_state.login=False

if "pedidos" not in st.session_state:
    st.session_state.pedidos=[]

if not st.session_state.login:

    c1,c2,c3=st.columns([1,1,1])

    with c2:

        st.markdown("# 🍕 Pizza Control")

        user=st.text_input(
            "Usuário"
        )

        senha=st.text_input(
            "Senha",
            type="password"
        )

        if st.button(
            "ENTRAR",
            use_container_width=True
        ):

            if (
                user==USUARIO
                and
                senha==SENHA
            ):

                st.session_state.login=True
                st.rerun()

            else:
                st.error(
                    "Login inválido"
                )

    st.stop()

abas=st.tabs([
"🍕 PEDIDOS",
"👨‍🍳 COZINHA",
"📊 DASHBOARD"
])

sabores=[
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

with abas[0]:

    st.title("Novo Pedido")

    a,b=st.columns(2)

    mesa=a.selectbox(
        "Mesa",
        range(1,51)
    )

    pizza=b.selectbox(
        "Pizza",
        sabores
    )

    qtd=st.number_input(
        "Quantidade",
        1,
        10
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

            "qtd":
            qtd,

            "status":
            "PREPARANDO"

        })

        st.success(
            "Pedido enviado"
        )

with abas[1]:

    st.title(
        "👨‍🍳 Produção"
    )

    preparar=[]
    prontos=[]

    for i,p in enumerate(
        st.session_state.pedidos
    ):

        if (
            p["status"]
            ==
            "PREPARANDO"
        ):
            preparar.append(
                (i,p)
            )

        else:
            prontos.append(
                (i,p)
            )

    c1,c2=st.columns(2)

    with c1:

        st.subheader(
            "EM PRODUÇÃO"
        )

        for i,p in preparar:

            st.markdown(
f"""
<div class='card'>

Mesa {p['mesa']}

🍕 {p['pizza']}

Qtd {p['qtd']}

</div>
""",
unsafe_allow_html=True
)

            if st.button(
                f"Finalizar {i}"
            ):

                st.session_state.pedidos[i][
                    "status"
                ]="PRONTO"

                st.rerun()

    with c2:

        st.subheader(
            "FINALIZADOS"
        )

        for i,p in prontos:

            st.success(
f"""
Mesa {p['mesa']}
—
{p['pizza']}
"""
            )

with abas[2]:

    st.title(
        "📊 Dashboard"
    )

    if st.session_state.pedidos:

        df=pd.DataFrame(
            st.session_state.pedidos
        )

        m1,m2,m3=st.columns(3)

        m1.metric(
            "Pedidos",
            len(df)
        )

        m2.metric(
            "Pizzas",
            df.qtd.sum()
        )

        pico=(
            df["hora"]
            .dt.hour
            .mode()[0]
        )

        m3.metric(
            "Pico",
            f"{pico}:00"
        )

        top=(
            df
            .groupby(
                "pizza"
            )[
                "qtd"
            ]
            .sum()
            .reset_index()
        )

        fig=px.bar(
            top,
            x="pizza",
            y="qtd",
            title="Mais Pedidas"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Sem pedidos"
        )

if st.sidebar.button(
"Sair"
):

    st.session_state.login=False

    st.rerun()