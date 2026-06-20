import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Pizza Control",layout="wide")

st.markdown("""
<style>
[data-testid='stSidebar']{background:#111!important;}
[data-testid='stSidebar'] *{color:white!important;}
div.stButton>button{background:#B71C1C!important;color:white!important;border-radius:16px;height:90px;font-weight:700;}
@media (max-width:768px){div.stButton>button{height:70px;font-size:13px;}}
</style>
""",unsafe_allow_html=True)

if 'pedidos' not in st.session_state: st.session_state.pedidos=[]
if 'item' not in st.session_state: st.session_state.item=None

sabores=[
'NAPOLITANA','CAMARÃO','CAIPIRA','MINEIRA','MODA DA CASA','STROGONOFF',
'CALABRESA','PORTUGUESA','FRANGO CATUPIRY','4 QUEIJOS','MEXICANA',
'MACARRÃO BOLONHESA','MACARRÃO 4 QUEIJOS','MACARRÃO PICANTE','MACARRÃO MODA DA CASA'
]

st.title('🍕 Pizza Control')

colunas=4
for i in range(0,len(sabores),colunas):
 linhas=sabores[i:i+colunas]
 cols=st.columns(len(linhas),gap='small')
 for col,s in zip(cols,linhas):
  with col:
   if st.button(s,use_container_width=True):
    st.session_state.item=s

if st.session_state.item:
 st.success(f'Selecionado: {st.session_state.item}')
 mesa=st.selectbox('Mesa',range(1,31))
 if st.button('Enviar para Cozinha',use_container_width=True):
  st.session_state.pedidos.append({'pizza':st.session_state.item,'mesa':mesa,'hora':datetime.now()})
  st.rerun()
