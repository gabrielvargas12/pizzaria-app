import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Controle de Pedidos", layout="wide")
USUARIO="gilvan"
SENHA="gilvan2008"
if "logado" not in st.session_state: st.session_state.logado=False
if "pedidos" not in st.session_state: st.session_state.pedidos=[]
if "pizza_escolhida" not in st.session_state: st.session_state.pizza_escolhida=None

sabores=["NAPOLITANA","CAMARÃO","CAIPIRA","MINEIRA","MODA DA CASA","STROGONOFF","CALABRESA","PORTUGUESA","FRANGO CATUPIRY","4 QUEIJOS","MEXICANA"]

if not st.session_state.logado:
 st.title("🍕 Pizza Control")
 u=st.text_input("Usuário")
 s=st.text_input("Senha",type="password")
 if st.button("Entrar"):
  if u==USUARIO and s==SENHA:
   st.session_state.logado=True
   st.rerun()
 st.stop()

menu=st.sidebar.radio("MENU",["🍕 NOVO PEDIDO","👨‍🍳 COZINHA","📊 DASHBOARD"])

if menu=="🍕 NOVO PEDIDO":
 st.title("🍕 Escolha")
 for sabor in sabores:
  if st.button(sabor): st.session_state.pizza_escolhida=sabor
 if st.session_state.pizza_escolhida:
  mesa=st.selectbox("Mesa",range(1,31))
  if st.button("Enviar"):
   st.session_state.pedidos.append({"hora":datetime.now(),"mesa":mesa,"pizza":st.session_state.pizza_escolhida,"status":"PREPARANDO"})
   st.rerun()
elif menu=="👨‍🍳 COZINHA":
 st.title("👨‍🍳 Cozinha")
 st.write(st.session_state.pedidos)
else:
 st.title("📊 Dashboard")
