import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Controle de Pedidos",
    layout="wide"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* BASE */

html,
body,
[class*="css"]{
font-family:'Poppins',sans-serif;
}

/* FUNDO */

.stApp{
background-image:url(
"https://images.unsplash.com/photo-1513104890138-7c749659a591"
);
background-size:cover;
background-position:center;
background-attachment:fixed;
}

/* CAMADA ESCURA */

.stApp::before{

content:"";

position:fixed;

top:0;
left:0;
right:0;
bottom:0;

background:rgba(
0,
0,
0,
0.78
);

z-index:-1;

}

/* TITULO PRINCIPAL */

h1{

color:#FFD54F !important;

font-weight:700;

text-shadow:
2px 2px 8px rgba(
0,
0,
0,
0.9
);

}

/* SUBTITULOS */

h2,
h3,
h4,
h5,
h6{

color:white !important;

}

/* TEXTOS */

p,
span,
label,
small,
strong{

color:white !important;

}

/* SIDEBAR */

[data-testid="stSidebar"]{

background:#141821;

}

[data-testid="stSidebar"] *{

color:white !important;

}

/* LOGIN */

.stTextInput input{

background:white !important;

color:black !important;

border-radius:10px;

padding:10px;

}

.stTextInput label{

color:white !important;

}

/* SELECT */

[data-baseweb="select"]{

background:#23262E !important;

border-radius:10px;

}

[data-baseweb="select"] span{

color:white !important;

}

[role="listbox"]{

background:white !important;

}

[role="option"]{

color:black !important;

}

/* BOTÕES */

div.stButton > button{

height:78px;

border-radius:18px;

background:#B22222;

color:white !important;

font-size:17px;

font-weight:700;

border:none;

transition:0.2s;

}

div.stButton > button:hover{

background:#D32F2F;

transform:translateY(-2px);

}

/* DASHBOARD */

[data-testid="stMetricValue"],
[data-testid="stMetricLabel"]{

color:white !important;

}

/* TABELAS */

table,
thead,
tbody,
th,
td{

color:white !important;

background:transparent !important;

}

/* ALERTAS */

[data-testid="stAlertContainer"]{

color:white !important;

}

/* ÍCONES */

svg{

fill:white !important;

color:white !important;

}

/* MENU LATERAL ☰ */

button[kind="header"]{

background:transparent !important;

}

/* COR PADRÃO */

button[kind="header"] svg{

fill:black !important;

stroke:black !important;

color:black !important;

}

/* QUANDO MENU ESTIVER ESCURO */

[data-testid="stSidebar"] button[kind="header"] svg{

fill:white !important;

stroke:white !important;

color:white !important;

}

/* PLACEHOLDER */

input::placeholder{

color:#666 !important;

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

        st.title("🍕 Controle de Pedidos ")

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

        st.markdown(
f"""

 Selecionado: {st.session_state.pizza_escolhida}

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

elif menu == "👨‍🍳 COZINHA":

```
st.title("👨‍🍳 Cozinha")

pedidos = st.session_state.pedidos

preparando = [
    (i, p)
    for i, p in enumerate(pedidos)
    if p["status"] == "PREPARANDO"
]

prontos = [
    (i, p)
    for i, p in enumerate(pedidos)
    if p["status"] == "PRONTO"
]

c1, c2 = st.columns(2)

with c1:

    st.subheader("🔥 PREPARANDO")

    grupos = {}

    for i, p in preparando:

        sabor = p["pizza"]

        if sabor not in grupos:
            grupos[sabor] = []

        grupos[sabor].append((i, p))

    for sabor, itens in grupos.items():

        mesas = []
        horas = []
        ids = []

        for idx, p in itens:

            mesas.append(
                str(p["mesa"])
            )

            horas.append(
                p["hora"].strftime("%H:%M")
            )

            ids.append(idx)

        texto = f"""
```

 {sabor}

texto = (
f"🍕 {sabor}\n\n"
f"📦 {len(itens)} pedidos\n\n"
f"🪑 Mesas:\n"
f"{' • '.join(mesas)}\n\n"
f"🕒 {', '.join(horas)}"
)
"""

```
        st.info(texto)

        if st.button(
            f"FINALIZAR {sabor}",
            key=f"finalizar_{sabor}"
        ):

            for idx in ids:

                st.session_state.pedidos[idx][
                    "status"
                ] = "PRONTO"

            st.rerun()

with c2:

    st.subheader("✅ PRONTOS")

    finalizados = {}

    for i, p in prontos:

        sabor = p["pizza"]

        if sabor not in finalizados:
            finalizados[sabor] = 0

        finalizados[sabor] += 1

    for sabor, qtd in finalizados.items():

        texto = f"""
```

 {sabor}

f"✅ {qtd} concluídos"
"""

```
        st.success(texto)
```

# DASHBOARD

elif menu == "📊 DASHBOARD":

```
st.title("📊 Dashboard")

if len(st.session_state.pedidos):

    df = pd.DataFrame(
        st.session_state.pedidos
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Pedidos",
        len(df)
    )

    c2.metric(

        "Prontos",

        len(
            df[
                df["status"] == "PRONTO"
            ]
        )
    )

    c3.metric(

        "Preparando",

        len(
            df[
                df["status"] == "PREPARANDO"
            ]
        )
    )

    pizza = (
        df["pizza"]
        .value_counts()
        .head(10)
    )

    st.subheader(
        "🍕 Mais Pedidas"
    )

    st.bar_chart(
        pizza
    )

else:

    st.info(
        "Nenhum pedido ainda"
    )
```
