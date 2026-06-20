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
"MEXICANA",
"🍝 MACARRÃO BOLONHESA",
"🍝 MACARRÃO 4 QUEIJOS",
"🌶️ MACARRÃO PICANTE",
"🍝 MACARRÃO MODA DA CASA"

]    

# PEDIDOS

if menu=="🍕 NOVO PEDIDO":

    st.title("🍕 Escolha o Pedido")

    if "pizza_escolhida" not in st.session_state:
        st.session_state.pizza_escolhida=None

    colunas=4

    linhas=[
        sabores[i:i+colunas]
        for i in range(
            0,
            len(sabores),
            colunas
        )
    ]

    for linha in linhas:

        cols=st.columns(
            len(linha)
        )

        for col,sabor in zip(
            cols,
            linha
        ):

            with col:

                if st.button(

                    sabor,

                    use_container_width=True,

                    key=sabor

                ):

                    st.session_state.pizza_escolhida=sabor

    if st.session_state.pizza_escolhida:

        st.divider()

        st.success(
            f"Selecionado: {st.session_state.pizza_escolhida}"
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

    pedidos=st.session_state.pedidos

    preparando=[
        (i,p)
        for i,p in enumerate(
            pedidos
        )
        if p["status"]=="PREPARANDO"
    ]

    prontos=[
        (i,p)
        for i,p in enumerate(
            pedidos
        )
        if p["status"]=="PRONTO"
    ]

    c1,c2=st.columns(2)

    with c1:

        st.subheader(
            "🔥 PREPARANDO"
        )

        grupos={}

        for i,p in preparando:

            sabor=p["pizza"]

            if sabor not in grupos:

                grupos[sabor]=[]

            grupos[sabor].append(
                (i,p)
            )

        for sabor,itens in grupos.items():

            mesas=[]

            horas=[]

            ids=[]

            for idx,p in itens:

                mesas.append(
                    str(
                        p["mesa"]
                    )
                )

                horas.append(

                    p["hora"]
                    .strftime(
                        "%H:%M"
                    )

                )

                ids.append(
                    idx
                )

            st.info(

f"""
{sabor}

📦 {len(itens)} pedidos

🪑 Mesas:
{' • '.join(mesas)}

🕒 {' • '.join(horas)}
"""

            )

            if st.button(

                f"FINALIZAR {sabor}",

                key=sabor

            ):

                for idx in ids:

                    st.session_state.pedidos[
                        idx
                    ][
                        "status"
                    ]="PRONTO"

                st.rerun()

    with c2:

        st.subheader(
            "✅ PRONTOS"
        )

        finalizados={}

        for i,p in prontos:

            sabor=p["pizza"]

            if sabor not in finalizados:

                finalizados[sabor]=0

            finalizados[sabor]+=1

        for sabor,qtd in finalizados.items():

            st.success(

f"""
{sabor}

✅ {qtd} concluídos
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
            " Mais Pedidas"
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
