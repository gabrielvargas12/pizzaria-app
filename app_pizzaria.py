import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Pizza Control",layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
html,body,[class*="css"]{font-family:Poppins,sans-serif;}
.stApp{background-image:url('https://images.unsplash.com/photo-1513104890138-7c749659a591');background-size:cover;background-position:center;}
.stApp:before{content:'';position:fixed;inset:0;background:rgba(0,0,0,.78);z-index:-1;}
[data-testid='stSidebar']{background:#111!important}
[data-testid='stSidebar'] *{color:white!important}
h1{color:#FFD54F!important}
input{background:white!important;color:black!important}
div.stButton>button{background:#B71C1C!important;color:white!important;border-radius:16px;height:85px;font-weight:700;width:100%}
[data-testid='stMetricValue'],[data-testid='stMetricLabel']{color:white!important}
@media(max-width:768px){div.stButton>button{height:72px;font-size:13px}}
</style>
""",unsafe_allow_html=True)

USER='gilvan'
PASS='gilvan2008'

for k,v in [('logado',False),('pedidos',[]),('selecao',None)]:
    if k not in st.session_state:
        st.session_state[k]=v

sabores=["NAPOLITANA","CAMARÃO","CAIPIRA","MINEIRA","MODA DA CASA","STROGONOFF","CALABRESA","PORTUGUESA","FRANGO CATUPIRY","4 QUEIJOS","MEXICANA","MACARRÃO BOLONHESA","MACARRÃO 4 QUEIJOS","MACARRÃO PICANTE","MACARRÃO MODA DA CASA"]

if not st.session_state.logado:
    c1,c2,c3=st.columns([1,1,1])
    with c2:
        st.title('🍕 Pizza Control')
        u=st.text_input('Usuário')
        s=st.text_input('Senha',type='password')
        if st.button('Entrar'):
            if u==USER and s==PASS:
                st.session_state.logado=True
                st.rerun()
            st.error('Login inválido')
    st.stop()

menu=st.sidebar.radio('MENU',['🍕 NOVO PEDIDO','👨‍🍳 COZINHA','📊 DASHBOARD'])

if menu=='🍕 NOVO PEDIDO':
    st.title('🍕 Escolha o Pedido')
    cols=4
    for i in range(0,len(sabores),cols):
        linha=st.columns(min(cols,len(sabores)-i))
        for c,s in zip(linha,sabores[i:i+cols]):
            with c:
                if st.button(s,use_container_width=True,key=s):
                    st.session_state.selecao=s

    if st.session_state.selecao:
        st.success(f'Item selecionado: {st.session_state.selecao}')
        mesa=st.selectbox('Mesa',range(1,31))
        if st.button('Enviar para Cozinha'):
            st.session_state.pedidos.append({'pizza':st.session_state.selecao,'mesa':mesa,'hora':datetime.now(),'status':'PREPARANDO'})
            st.session_state.selecao=None
            st.rerun()

elif menu=='👨‍🍳 COZINHA':
    st.title('👨‍🍳 Controle de Pedidos')
    grupos={}
    for idx,p in enumerate(st.session_state.pedidos):
        if p['status']=='PREPARANDO':
            grupos.setdefault(p['pizza'],[]).append((idx,p))

    st.subheader('Preparando')
    for sabor,itens in grupos.items():
        mesas=' • '.join(str(x[1]['mesa']) for x in itens)
        st.info(f'🍕 {sabor}\n\n📦 {len(itens)} pedidos\n🪑 Mesas: {mesas}')
        if st.button(f'FINALIZAR {sabor}'):
            for idx,_ in itens:
                st.session_state.pedidos[idx]['status']='PRONTO'
            st.rerun()

    st.subheader('Prontos')
    prontos={}
    for p in st.session_state.pedidos:
        if p['status']=='PRONTO':
            prontos[p['pizza']]=prontos.get(p['pizza'],0)+1
    for s,q in prontos.items():
        st.success(f'{s} • {q} concluídos')

elif menu=='📊 DASHBOARD':
    st.title('📊 Dashboard')
    if st.session_state.pedidos:
        df=pd.DataFrame(st.session_state.pedidos)
        c1,c2,c3=st.columns(3)
        c1.metric('Pedidos',len(df))
        c2.metric('Prontos',(df.status=='PRONTO').sum())
        hora=df.hora.dt.hour.mode()[0]
        c3.metric('Hora Pico',f'{hora}:00')
        st.subheader('🍕 Mais Pedidas')
        st.plotly_chart(px.bar(df['pizza'].value_counts().reset_index(),x='pizza',y='count'),use_container_width=True)
        st.dataframe(df)
    else:
        st.info('Sem pedidos')

if st.sidebar.button('Sair'):
    st.session_state.logado=False
    st.rerun()
