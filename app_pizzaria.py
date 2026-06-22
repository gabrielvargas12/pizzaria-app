"""
Sistema Profissional de Gestão de Pizzaria
Desenvolvido para alta performance e escalabilidade
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from database import Database
from config import Config, UserRole, OrderStatus, PAYMENT_METHODS, COLORS
from typing import Dict, Optional
import os

# ==================== CONFIGURAÇÃO ====================
st.set_page_config(
    page_title="🍕 Gestão de Pizzaria",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "Report a bug": "https://github.com",
        "About": "Sistema Profissional de Gestão de Pizzaria v1.0"
    }
)

# CSS customizado
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .status-pending { background-color: #ff6b6b; }
    .status-preparing { background-color: #ffa500; }
    .status-ready { background-color: #4ecdc4; }
    .status-served { background-color: #95e1d3; }
    .status-paid { background-color: #28a745; }
    </style>
""", unsafe_allow_html=True)

# ==================== INICIALIZAÇÃO ====================
if "db" not in st.session_state:
    st.session_state.db = Database()

db = st.session_state.db

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "current_order" not in st.session_state:
    st.session_state.current_order = None
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# ==================== AUTENTICAÇÃO ====================
def login_page():
    """Página de login profissional"""
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center'>🍕</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center'>Sistema de Pizzaria</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray'>Versão Profissional</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        username = st.text_input("👤 Usuário", key="login_user")
        password = st.text_input("🔐 Senha", type="password", key="login_pass")
        
        col_login, col_help = st.columns(2)
        
        with col_login:
            if st.button("✅ Entrar", use_container_width=True, type="primary"):
                user = db.verify_user(username, password)
                
                if user:
                    st.session_state.user = user
                    st.success(f"Bem-vindo, {user['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha inválidos")
        
        with col_help:
            st.info("📝 Credenciais padrão:\nAdmin: admin/admin2024\nCozinha: cozinha/staff2024")

# ==================== FUNÇÕES AUXILIARES ====================
def logout():
    """Logout do usuário"""
    st.session_state.user = None
    st.session_state.page = "dashboard"
    st.session_state.current_order = None
    st.rerun()

        else:
            st.error(
                "Usuário ou senha inválidos"
            )

    st.stop()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 👤 Usuário Conectado")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**{st.session_state.user['name']}**")
        role_display = {
            "admin": "👑 Administrador",
            "manager": "📊 Gerente",
            "kitchen": "👨‍🍳 Cozinha",
            "waiter": "🍽️ Garçom"
        }
        st.caption(role_display.get(st.session_state.user['role'], st.session_state.user['role']))
    
    with col2:
        if st.button("Sair", use_container_width=True):
            logout()
    
    st.markdown("---")
    
    # Navegação baseada no role
    st.markdown("### 📋 Menu")
    
    role = st.session_state.user['role']
    
    if role in ["admin", "manager"]:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
        if st.button("📝 Novo Pedido", use_container_width=True):
            st.session_state.page = "new_order"
        if st.button("📋 Pedidos", use_container_width=True):
            st.session_state.page = "orders"
    
    if role == "kitchen":
        if st.button("👨‍🍳 Pedidos Cozinha", use_container_width=True):
            st.session_state.page = "kitchen"
    
    if role in ["admin", "manager", "waiter"]:
        if st.button("💳 Pagamentos", use_container_width=True):
            st.session_state.page = "payments"
    
    if role == "admin":
        if st.button("⚙️ Administração", use_container_width=True):
            st.session_state.page = "admin"
    
    st.markdown("---")
    st.markdown("**v1.0** | © 2024 Pizzaria Pro")

# ==================== PÁGINAS ====================

# DASHBOARD
if st.session_state.page == "dashboard" and has_permission("view_reports"):
    st.title("📊 Dashboard")
    
    # Seletor de período
    col1, col2, col3 = st.columns(3)
    with col1:
        days = st.selectbox("Período", [7, 30, 90], index=1)
    
    # Dados do relatório
    report = db.get_sales_report(days)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Receita Total",
            format_currency(report['total_revenue']),
            delta=f"{days} dias"
        )
    
    with col2:
        st.metric(
            "📦 Pedidos",
            f"{report['total_orders']:,}".replace(",", ".")
        )
    
    with col3:
        avg = report['average_order']
        st.metric(
            "📈 Ticket Médio",
            format_currency(avg)
        )
    
    with col4:
        if report['total_orders'] > 0:
            st.metric(
                "⭐ Eficiência",
                f"{(report['total_revenue'] / report['total_orders'] * 100 / avg) if avg > 0 else 0:.0f}%"
            )
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        if report['top_items']:
            df_items = pd.DataFrame(report['top_items'])
            fig = px.bar(df_items, x='name', y='qty', title="🍕 Pizzas Mais Vendidas",
                        labels={'name': 'Produto', 'qty': 'Quantidade'})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if report['top_items']:
            df_revenue = pd.DataFrame(report['top_items'])
            fig = px.pie(df_revenue, values='revenue', names='name', title="💰 Faturamento por Produto")
            st.plotly_chart(fig, use_container_width=True)

# NOVO PEDIDO
elif st.session_state.page == "new_order" and has_permission("create_order"):
    st.title("📝 Novo Pedido")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Dados do Pedido")
        
        table_number = st.selectbox(
            "🪑 Mesa",
            range(1, 31),
            format_func=lambda x: f"Mesa {x}"
        )
        
        notes = st.text_area("📝 Observações", height=100)
        
        st.markdown("---")
        st.subheader("Adicionar Itens")
        
        menu_items = db.get_menu()
        
        if menu_items:
            categories = sorted(set(item['category'] for item in menu_items))
            category = st.selectbox("📂 Categoria", categories)
            
            items_in_category = [item for item in menu_items if item['category'] == category]
            
            item_names = {item['id']: f"{item['name']} - {format_currency(item['price'])}" 
                         for item in items_in_category}
            
            selected_item_id = st.selectbox("🍕 Produto", item_names.keys(), 
                                           format_func=lambda x: item_names.get(x, ""))
            
            quantity = st.number_input("Quantidade", min_value=1, value=1)
            item_notes = st.text_input("Observações do item (ex: sem cebola)")
            
            if st.button("➕ Adicionar ao Pedido", type="primary", use_container_width=True):
                if st.session_state.current_order is None:
                    st.session_state.current_order = db.create_order(table_number, st.session_state.user['id'], notes)
                
                db.add_order_item(st.session_state.current_order, selected_item_id, quantity, item_notes)
                st.success("Item adicionado!")
                st.rerun()
    
    with col2:
        st.subheader("📋 Resumo do Pedido")
        
        if st.session_state.current_order:
            summary = create_order_summary(st.session_state.current_order)
            
            if summary['items']:
                st.write(f"**Mesa {table_number}** | Total: {summary['item_count']} itens")
                
                for item in summary['items']:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"🍕 {item['menu_name']}")
                        if item['notes']:
                            st.caption(f"📝 {item['notes']}")
                    with col2:
                        st.write(f"x{item['quantity']}")
                    with col3:
                        st.write(f"{format_currency(item['price'] * item['quantity'])}")
                
                st.markdown("---")
                st.metric("💰 Total", format_currency(summary['total']))
                
                col_confirm, col_cancel = st.columns(2)
                
                with col_confirm:
                    if st.button("✅ Confirmar Pedido", type="primary", use_container_width=True):
                        st.success(f"Pedido #{st.session_state.current_order} enviado para a cozinha!")
                        st.session_state.current_order = None
                        st.rerun()
                
                with col_cancel:
                    if st.button("❌ Cancelar", use_container_width=True):
                        st.session_state.current_order = None
                        st.rerun()
            else:
                st.info("Nenhum item adicionado ainda")
        else:
            st.info("Selecione uma mesa e comece a adicionar itens")

# PEDIDOS
elif st.session_state.page == "orders" and has_permission("create_order"):
    st.title("📋 Gerenciamento de Pedidos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Filtro Status",
            ["Todos", "Pendente", "Preparando", "Pronto", "Servido", "Pago"]
        )
    
    with col2:
        table_filter = st.selectbox(
            "Filtro Mesa",
            [None] + list(range(1, 31)),
            format_func=lambda x: "Todas" if x is None else f"Mesa {x}"
        )
    
    # Buscar pedidos
    status_param = None if status_filter == "Todos" else status_filter
    orders = db.get_orders(status=status_param, table_number=table_filter)
    
    if orders:
        for order in orders:
            with st.expander(f"Pedido #{order['id']} - Mesa {order['table_number']} - {order['status']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Criado em:** {order['created_at']}")
                    st.write(f"**Status:** {order['status']}")
                
                with col2:
                    summary = create_order_summary(order['id'])
                    st.write(f"**Itens:** {summary['item_count']}")
                    st.write(f"**Total:** {format_currency(summary['total'])}")
                
                with col3:
                    if order['notes']:
                        st.write(f"**Observações:** {order['notes']}")
                
                st.markdown("---")
                
                # Items do pedido
                st.write("**Itens do Pedido:**")
                for item in db.get_order_items(order['id']):
                    st.write(f"- {item['menu_name']} x{item['quantity']} ({format_currency(item['price'] * item['quantity'])})")
                    if item['notes']:
                        st.caption(f"  📝 {item['notes']}")
                
                # Ações
                col1, col2, col3 = st.columns(3)
                
                if order['status'] != "Pago":
                    with col1:
                        if st.button(f"Marcar como Pronto", key=f"ready_{order['id']}", use_container_width=True):
                            db.update_order_status(order['id'], "Pronto")
                            st.rerun()
                    
                    with col2:
                        if st.button(f"Marcar como Servido", key=f"served_{order['id']}", use_container_width=True):
                            db.update_order_status(order['id'], "Servido")
                            st.rerun()
                    
                    with col3:
                        if st.button(f"Marcar como Cancelado", key=f"cancel_{order['id']}", use_container_width=True):
                            db.update_order_status(order['id'], "Cancelado")
                            st.rerun()
    else:
        st.info("Nenhum pedido encontrado")

# COZINHA
elif st.session_state.page == "kitchen" and has_permission("view_pending_orders"):
    st.title("👨‍🍳 Painel da Cozinha")
    
    # Auto-refresh a cada 10 segundos
    import time
    st.write("*Sistema se atualiza automaticamente a cada 10 segundos*")
    
    col1, col2, col3 = st.columns(3)
    
    # Pedidos por status
    pending = db.get_orders(status="Pendente")
    preparing = db.get_orders(status="Preparando")
    ready = db.get_orders(status="Pronto")
    
    with col1:
        st.metric("⏳ Pendente", len(pending))
    with col2:
        st.metric("🔥 Preparando", len(preparing))
    with col3:
        st.metric("✅ Pronto", len(ready))
    
    st.markdown("---")
    
    # Pedidos pendentes e preparando
    all_working = pending + preparing
    
    if all_working:
        for order in all_working:
            status_color = "🟡" if order['status'] == "Pendente" else "🟠"
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"### {status_color} Mesa {order['table_number']}")
                    
                    for item in db.get_order_items(order['id']):
                        st.write(f"🍕 **{item['menu_name']}** x{item['quantity']}")
                        if item['notes']:
                            st.caption(f"📝 {item['notes']}")
                
                with col2:
                    created = datetime.fromisoformat(order['created_at'])
                    elapsed = datetime.now() - created
                    minutes = int(elapsed.total_seconds() / 60)
                    st.metric("⏱️ Tempo", f"{minutes}min")
                
                with col3:
                    if order['status'] == "Pendente":
                        if st.button(f"Iniciando...", key=f"start_{order['id']}", use_container_width=True, type="primary"):
                            db.update_order_status(order['id'], "Preparando")
                            st.rerun()
                    
                    else:
                        if st.button(f"✅ Pronto", key=f"ready_{order['id']}", use_container_width=True, type="primary"):
                            db.update_order_status(order['id'], "Pronto")
                            st.rerun()
    else:
        st.success("✅ Nenhum pedido para preparar!")
    
    st.markdown("---")
    
    # Pedidos prontos
    if ready:
        st.markdown("### ✅ Pedidos Prontos para Servir")
        for order in ready:
            st.write(f"🟢 Mesa {order['table_number']}")

# PAGAMENTOS
elif st.session_state.page == "payments" and has_permission("process_payment"):
    st.title("💳 Processamento de Pagamentos")
    
    orders = db.get_orders(status="Servido")
    
    if orders:
        st.write(f"**{len(orders)} pedido(s) pronto(s) para pagamento**")
        
        for order in orders:
            with st.expander(f"Mesa {order['table_number']} - Pedido #{order['id']}", expanded=False):
                summary = create_order_summary(order['id'])
                
                st.write("**Itens:**")
                for item in summary['items']:
                    st.write(f"- {item['menu_name']} x{item['quantity']}: {format_currency(item['price'] * item['quantity'])}")
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("💰 Total", format_currency(summary['total']))
                
                with col2:
                    payment_method = st.selectbox(
                        "Método de Pagamento",
                        PAYMENT_METHODS,
                        key=f"method_{order['id']}"
                    )
                
                if st.button(f"✅ Confirmar Pagamento", key=f"pay_{order['id']}", use_container_width=True, type="primary"):
                    db.record_payment(order['id'], summary['total'], payment_method)
                    st.success(f"Pagamento processado! Total: {format_currency(summary['total'])}")
                    st.rerun()
    else:
        st.info("Nenhum pedido aguardando pagamento")

# ADMIN
elif st.session_state.page == "admin" and has_permission("manage_users"):
    st.title("⚙️ Administração")
    
    tab1, tab2, tab3 = st.tabs(["👥 Usuários", "📋 Menu", "🔍 Logs"])
    
    with tab1:
        st.subheader("Gerenciar Usuários")
        st.info("Funcionalidade em desenvolvimento")
    
    with tab2:
        st.subheader("Gerenciar Menu")
        
        menu = db.get_menu()
        df_menu = pd.DataFrame(menu)
        
        st.dataframe(df_menu[['name', 'price', 'category', 'active']], use_container_width=True)
        
        st.markdown("---")
        st.write("**Adicionar novo item:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Nome")
            price = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
        
        with col2:
            category = st.selectbox("Categoria", ["Pizza", "Bebida", "Sobremesa", "Outro"])
        
        with col3:
            description = st.text_area("Descrição")
    
    with tab3:
        st.write("Logs de sistema")
        st.info("Implementação futura")

st.markdown("---")
st.caption("Sistema Profissional de Gestão de Pizzaria | v1.0")
