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
background:#FFFFFF;
color:black;
}

.block-container{
padding-top:1rem;
}

div.stButton > button{
height:80px;
font-size:18px;
border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# LOGIN

USUARIO="gilvan"
SENHA="gilvan2008"

if "logado" not in st.session_state:
    st.session_state.logado=False

if "pedidos" not in st.session_state:
    st.session_state.pedidos=[]

if "pizza_escolhida" not in st.session_state:
    st.session_state.pizza_escolhida=None

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

# MENU

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

    
# MACARRÃO

"🍝 MACARRÃO BOLONHESA",
"🍝 MACARRÃO 4 QUEIJOS",
"🌶️ MACARRÃO PICANTE",
"🍝 MACARRÃO MODA DA CASA"

]    

# PEDIDOS

if menu=="🍕 NOVO PEDIDO":

    st.title(
        "🍕 Escolha a Pizza"
    )

    colunas=3

    for i in range(
        0,
        len(sabores),
        colunas
    ):

        cols=st.columns(
            colunas
        )

        grupo=sabores[
            i:
            i+colunas
        ]

        for coluna,sabor in zip(
            cols,
            grupo
        ):

            with coluna:

                if st.button(

                    f" {sabor}",

                    use_container_width=True

                ):

                    st.session_state.pizza_escolhida=sabor

    if st.session_state.pizza_escolhida:

        st.divider()

        st.success(

f"""
Selecionada:

 {st.session_state.pizza_escolhida}
"""

        )

        mesa=st.selectbox(

            "Mesa",

            range(
                1,
                31
            )

        )

        if st.button(

            "Enviar para Cozinha",

            use_container_width=True

        ):

            st.session_state.pedidos.append({

                "hora":
                datetime.now(),

                "mesa":
                mesa,

                "pizza":
                st.session_state.pizza_escolhida,

                "status":
                "PREPARANDO"

            })

            st.session_state.pizza_escolhida=None

            st.success(
                "Pedido enviado"
            )

            st.rerun()

# COZINHA

elif menu=="👨‍🍳 COZINHA":

    st.title(
        "👨‍🍳 Cozinha"
    )

    preparar=[]
    pronto=[]

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

            pronto.append(
                (i,p)
            )

    c1,c2=st.columns(2)

    with c1:

        st.subheader(
            "🔥 PREPARANDO"
        )

        for i,p in preparar:

            st.info(

f"""
Mesa {p["mesa"]}

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

    with c2:

        st.subheader(
            "✅ PRONTOS"
        )

        for i,p in pronto:

            st.success(

f"""
Mesa {p["mesa"]}

🍕 {p["pizza"]}
"""

            )

# DASHBOARD

elif menu=="📊 DASHBOARD":

    st.title(
        "📊 Dashboard"
    )

    if len(
        st.session_state.pedidos
    ):

        df=pd.DataFrame(
            st.session_state.pedidos
        )

        c1,c2,c3=(
            st.columns(3)
        )

        c1.metric(
            "Pedidos",
            len(df)
        )

        c2.metric(

            "Prontos",

            (
                df[
                    "status"
                ]
                ==
                "PRONTO"
            ).sum()

        )

        hora=(
            df["hora"]
            .dt.hour
            .mode()[0]
        )

        c3.metric(
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
