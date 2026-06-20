import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Pizza Control", layout="wide")

st.markdown("""
<style>
.stApp{background:#121212;color:white;}
[data-testid='stSidebar']{background:#111 !important;}
[data-testid='stSidebar'] *{color:white !important;}
div.stButton>button{
background:#b71c1c !important;
color:white !important;
border-radius:16px;
height:88px;
font-weight:700;
width:100%;
}
input{background:white !important;color:black !important;}
</style>
""", unsafe_allow_html=True)

USUARIO='gilvan'
SENHA='gilvan2008'

for k,v in [('logado',False),('pedidos',[]),('selecao',None)]:
    if k not in st.session_state:
        st.session_state[k]=v
hora = datetime.now(
    ZoneInfo("America/Sao_Paulo")
).strftime("%H:%M:%S")

st.sidebar.markdown(
    f"""
## 🕒 Brasília
### {hora}
"""
)

sabores=[
' NAPOLITANA',' CAMARÃO',' CAIPIRA',' MINEIRA',' MODA DA CASA',
' STROGONOFF',' CALABRESA',' PORTUGUESA',' FRANGO CATUPIRY',
' 4 QUEIJOS',' MEXICANA',
'🍝 MACARRÃO BOLONHESA','🍝 MACARRÃO 4 QUEIJOS',
'🍝 MACARRÃO PICANTE','🍝 MACARRÃO MODA DA CASA'
]

if not st.session_state.logado:
    st.title('🍕 Pizza Control')
    u=st.text_input('Usuário')
    s=st.text_input('Senha',type='password')
    if st.button('Entrar'):
        if u==USUARIO and s==SENHA:
            st.session_state.logado=True
            st.rerun()
    st.stop()

menu=st.sidebar.radio('MENU',['🍕 NOVO PEDIDO','👨‍🍳 COZINHA','📊 DASHBOARD'])

if menu=='🍕 NOVO PEDIDO':
    st.title('Escolha o Pedido')
    cols=4
    for i in range(0,len(sabores),cols):
        c=st.columns(min(cols,len(sabores)-i))
        for col,s in zip(c,sabores[i:i+cols]):
            with col:
                if st.button(s,key=s,use_container_width=True):
                    st.session_state.selecao=s
    if st.session_state.selecao:
        st.success(f'Selecionado: {st.session_state.selecao}')
        mesa=st.selectbox('Mesa',range(1,31))
        if st.button('Enviar para Cozinha'):
            st.session_state.pedidos.append({'pizza':st.session_state.selecao,'mesa':mesa,'hora':datetime.now(),'status':'PREPARANDO'})
            st.rerun()

elif menu=='👨‍🍳 COZINHA':
    st.title('👨‍🍳 Controle de Pedidos')
    grupos={}
    for i,p in enumerate(st.session_state.pedidos):
        grupos.setdefault(p['pizza'],[]).append((i,p)) if p['status']=='PREPARANDO' else None
    for sabor,itens in grupos.items():
        mesas=' • '.join(str(x[1]['mesa']) for x in itens)
     texto = (
    f"{sabor}\n\n"
    f"📦 {len(itens)} pedidos\n\n"
    f"🪑 Mesas: {mesas}"
)

st.info(texto)
        if st.button(f'FINALIZAR {sabor}'):
            for idx,_ in itens:
                st.session_state.pedidos[idx]['status']='PRONTO'
            st.rerun()

else:
    st.title('📊 Dashboard')
    if st.session_state.pedidos:
        df=pd.DataFrame(st.session_state.pedidos)
        a,b,c=st.columns(3)
        a.metric('Pedidos',len(df))
        b.metric('Prontos',(df.status=='PRONTO').sum())
        c.metric('Preparando',(df.status=='PREPARANDO').sum())
        st.bar_chart(df['pizza'].value_counts())
        st.dataframe(df)
