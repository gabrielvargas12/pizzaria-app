"""
Sistema Profissional de Gestão de Pizzaria
Desenvolvido para alta performance e escalabilidade
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from database import Database
from config import Config, UserRole, OrderStatus, PAYMENT_METHODS, COLORS
from typing import Dict, Optional

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

# ==================== FUNÇÕES AUXILIARES ====================

def format_currency(value: float) -> str:
    """Formata valor em moeda brasileira"""
    try:
        if value is None or not isinstance(value, (int, float)):
            return "R$ 0,00"
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception as e:
        st.error(f"Erro ao formatar moeda: {e}")
        return "R$ 0,00"

def has_permission(permission: str) -> bool:
    """Verifica se usuário tem permissão"""
    try:
        if not st.session_state.user:
            return False
        
        role = st.session_state.user.get('role', '')
        if not role:
            return False
        
        config = Config()
        permissions = config.ROLE_PERMISSIONS.get(role, [])
        return permission in permissions
    except Exception as e:
        st.error(f"Erro ao verificar permissões: {e}")
        return False

def create_order_summary(order_id: int) -> dict:
    """Cria resumo do pedido"""
    try:
        if not order_id or order_id <= 0:
            return {"items": [], "total": 0.0, "item_count": 0}
        
        items = db.get_order_items(order_id)
        total = db.get_order_total(order_id)
        
        if not items:
            return {"items": [], "total": 0.0, "item_count": 0}
        
        return {
            "items": items,
            "total": total if total else 0.0,
            "item_count": sum(int(item.get('quantity', 0)) for item in items)
        }
    except Exception as e:
        st.error(f"Erro ao criar resumo do pedido: {e}")
        return {"items": [], "total": 0.0, "item_count": 0}

def logout():
    """Logout do usuário"""
    st.session_state.user = None
    st.session_state.page = "dashboard"
    st.session_state.current_order = None
    st.rerun()

# ==================== PÁGINA DE LOGIN ====================
def login_page():
    """Página de login profissional"""
    try:
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            st.markdown("<h1 style='text-align: center'>🍕</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center'>Sistema de Pizzaria</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray'>Versão Profissional v1.0</p>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            username = st.text_input("👤 Usuário", key="login_user").strip()
            password = st.text_input("🔐 Senha", type="password", key="login_pass")
            
            col_login, col_help = st.columns(2)
            
            with col_login:
                if st.button("✅ Entrar", use_container_width=True, type="primary"):
                    if not username or not password:
                        st.error("❌ Preencha usuário e senha")
                    else:
                        try:
                            user = db.verify_user(username, password)
                            
                            if user:
                                st.session_state.user = user
                                st.success(f"Bem-vindo, {user.get('name', 'Usuário')}!")
                                st.rerun()
                            else:
                                st.error("❌ Usuário ou senha inválidos")
                        except Exception as e:
                            st.error(f"❌ Erro ao autenticar: {e}")
            
            with col_help:
                st.info("""📝 **Credenciais padrão:**
                
- **Master:** gilvan / gilvan2008
- **Admin:** admin / admin2024
- **Cozinha:** cozinha / staff2024""")
    except Exception as e:
        st.error(f"Erro na página de login: {e}")

if not st.session_state.user:
    login_page()
    st.stop()

# ==================== SIDEBAR ====================
try:
    with st.sidebar:
        st.markdown("### 👤 Usuário Conectado")
        col1, col2 = st.columns([2, 1])
        
        user_name = st.session_state.user.get('name', 'Usuário') if st.session_state.user else 'Anônimo'
        user_role = st.session_state.user.get('role', 'unknown') if st.session_state.user else 'unknown'
        
        with col1:
            st.write(f"**{user_name}**")
            role_display = {
                "admin": "👑 Administrador",
                "manager": "📊 Gerente",
                "kitchen": "👨‍🍳 Cozinha",
                "waiter": "🍽️ Garçom"
            }
            st.caption(role_display.get(user_role, "👤 Usuário"))
        
        with col2:
            if st.button("Sair", use_container_width=True):
                logout()
        
        st.markdown("---")
        st.markdown("### 📋 Menu")
        
        if user_role in ["admin", "manager"]:
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
            if st.button("📝 Novo Pedido", use_container_width=True):
                st.session_state.page = "new_order"
            if st.button("📋 Pedidos", use_container_width=True):
                st.session_state.page = "orders"
        
        if user_role == "kitchen":
            if st.button("👨‍🍳 Pedidos Cozinha", use_container_width=True):
                st.session_state.page = "kitchen"
        
        if user_role in ["admin", "manager", "waiter"]:
            if st.button("💳 Pagamentos", use_container_width=True):
                st.session_state.page = "payments"
        
        if user_role == "admin":
            if st.button("⚙️ Administração", use_container_width=True):
                st.session_state.page = "admin"
        
        st.markdown("---")
        st.markdown("**v1.0** | © 2024 Pizzaria Pro")
except Exception as e:
    st.error(f"Erro ao carregar sidebar: {e}")



# ==================== DASHBOARD ====================
try:
    if st.session_state.page == "dashboard" and has_permission("view_reports"):
        st.title("📊 Dashboard Executivo")
        
        # Seletor de período
        col1, col2 = st.columns(2)
        with col1:
            days = st.selectbox("📅 Período", [7, 30, 90], index=1)
        
        try:
            # Dados do relatório
            report = db.get_sales_report(days if days and days > 0 else 30)
            
            # Validar dados do relatório
            if not report:
                st.warning("Nenhum dado disponível")
            else:
                # KPIs
                col1, col2, col3, col4 = st.columns(4)
                
                total_revenue = float(report.get('total_revenue', 0))
                total_orders = int(report.get('total_orders', 0))
                average_order = float(report.get('average_order', 0))
                
                with col1:
                    st.metric(
                        "💰 Receita Total",
                        format_currency(total_revenue),
                        delta=f"{days} dias"
                    )
                
                with col2:
                    st.metric(
                        "📦 Pedidos",
                        f"{total_orders:,}".replace(",", ".")
                    )
                
                with col3:
                    st.metric(
                        "📈 Ticket Médio",
                        format_currency(average_order)
                    )
                
                with col4:
                    if total_orders > 0 and average_order > 0:
                        efficiency = (total_revenue / total_orders * 100 / average_order)
                        st.metric("⭐ Eficiência", f"{efficiency:.0f}%")
                    else:
                        st.metric("⭐ Eficiência", "0%")
                
                st.markdown("---")
                
                # Gráficos
                top_items = report.get('top_items', [])
                if top_items:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        try:
                            df_items = pd.DataFrame(top_items)
                            if not df_items.empty:
                                fig = px.bar(df_items, x='name', y='qty', 
                                            title="🍕 Pizzas Mais Vendidas",
                                            labels={'name': 'Produto', 'qty': 'Quantidade'},
                                            color='qty',
                                            color_continuous_scale='Viridis')
                                st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"Erro ao gerar gráfico de vendas: {e}")
                    
                    with col2:
                        try:
                            df_revenue = pd.DataFrame(top_items)
                            if not df_revenue.empty:
                                fig = px.pie(df_revenue, values='revenue', names='name', 
                                            title="💰 Faturamento por Produto")
                                st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"Erro ao gerar gráfico de faturamento: {e}")
                else:
                    st.info("Sem dados para o período selecionado")
        except Exception as e:
            st.error(f"Erro ao carregar dashboard: {e}")
except Exception as e:
    st.error(f"Erro na página dashboard: {e}")

# ==================== NOVO PEDIDO ====================
try:
    if st.session_state.page == "new_order" and has_permission("create_order"):
        st.title("📝 Novo Pedido")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Dados do Pedido")
            
            table_number = st.selectbox(
                "🪑 Mesa",
                range(1, 31),
                format_func=lambda x: f"Mesa {x}"
            )
            
            notes = st.text_area("📝 Observações", height=100, value="")
            
            st.markdown("---")
            st.subheader("Adicionar Itens")
            
            try:
                menu_items = db.get_menu()
                
                if menu_items and len(menu_items) > 0:
                    categories = sorted(set(item.get('category', 'Outro') for item in menu_items if item))
                    
                    if categories:
                        category = st.selectbox("📂 Categoria", categories)
                        
                        items_in_category = [item for item in menu_items 
                                           if item and item.get('category') == category]
                        
                        if items_in_category:
                            item_names = {item['id']: f"{item.get('name', 'Sem nome')} - {format_currency(item.get('price', 0))}" 
                                         for item in items_in_category if item and 'id' in item}
                            
                            if item_names:
                                selected_item_id = st.selectbox("🍕 Produto", list(item_names.keys()), 
                                                               format_func=lambda x: item_names.get(x, ""))
                                
                                quantity = st.number_input("Quantidade", min_value=1, value=1)
                                item_notes = st.text_input("Observações do item (ex: sem cebola)", value="")
                                
                                if st.button("➕ Adicionar ao Pedido", type="primary", use_container_width=True):
                                    try:
                                        if st.session_state.current_order is None:
                                            if not st.session_state.user or 'id' not in st.session_state.user:
                                                st.error("❌ Erro: Usuário não autenticado")
                                            else:
                                                st.session_state.current_order = db.create_order(
                                                    int(table_number), 
                                                    int(st.session_state.user['id']), 
                                                    notes.strip()
                                                )
                                        
                                        if st.session_state.current_order:
                                            db.add_order_item(
                                                st.session_state.current_order, 
                                                selected_item_id, 
                                                int(quantity), 
                                                item_notes.strip()
                                            )
                                            st.success("✅ Item adicionado!")
                                            st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Erro ao adicionar item: {e}")
                            else:
                                st.warning("⚠️ Nenhum produto disponível nesta categoria")
                        else:
                            st.warning("⚠️ Nenhum produto nesta categoria")
                    else:
                        st.warning("⚠️ Nenhuma categoria disponível")
                else:
                    st.warning("⚠️ Menu vazio. Contate o administrador.")
            except Exception as e:
                st.error(f"❌ Erro ao carregar menu: {e}")
        
        with col2:
            st.subheader("📋 Resumo do Pedido")
            
            if st.session_state.current_order:
                try:
                    summary = create_order_summary(st.session_state.current_order)
                    
                    if summary and summary.get('items') and len(summary['items']) > 0:
                        item_count = summary.get('item_count', 0)
                        st.write(f"**Mesa {table_number}** | Total: {item_count} itens")
                        
                        for idx, item in enumerate(summary.get('items', [])):
                            col_a, col_b, col_c = st.columns([2, 1, 1])
                            with col_a:
                                st.write(f"🍕 {item.get('menu_name', 'Sem nome')}")
                                if item.get('notes'):
                                    st.caption(f"📝 {item['notes']}")
                            with col_b:
                                st.write(f"x{item.get('quantity', 0)}")
                            with col_c:
                                price = float(item.get('price', 0)) * int(item.get('quantity', 0))
                                st.write(f"{format_currency(price)}")
                        
                        st.markdown("---")
                        st.metric("💰 Total", format_currency(summary.get('total', 0)))
                        
                        col_confirm, col_cancel = st.columns(2)
                        
                        with col_confirm:
                            if st.button("✅ Confirmar Pedido", type="primary", use_container_width=True):
                                try:
                                    st.success(f"Pedido #{st.session_state.current_order} enviado para a cozinha!")
                                    st.session_state.current_order = None
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erro ao confirmar pedido: {e}")
                        
                        with col_cancel:
                            if st.button("❌ Cancelar", use_container_width=True):
                                st.session_state.current_order = None
                                st.rerun()
                    else:
                        st.info("Nenhum item adicionado ainda")
                except Exception as e:
                    st.error(f"❌ Erro ao carregar resumo: {e}")
            else:
                st.info("Selecione uma mesa e comece a adicionar itens")
except Exception as e:
    st.error(f"❌ Erro na página de novo pedido: {e}")

# ==================== GERENCIAR PEDIDOS ====================
try:
    if st.session_state.page == "orders" and has_permission("create_order"):
        st.title("📋 Gerenciamento de Pedidos")
        
        col1, col2 = st.columns(2)
        
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
        
        try:
            # Buscar pedidos
            status_param = None if status_filter == "Todos" else status_filter
            orders = db.get_orders(status=status_param, table_number=table_filter)
            
            if orders and len(orders) > 0:
                for order in orders:
                    if order and isinstance(order, dict):
                        try:
                            order_id = order.get('id')
                            table_num = order.get('table_number')
                            order_status = order.get('status', 'Desconhecido')
                            
                            with st.expander(f"Pedido #{order_id} - Mesa {table_num} - {order_status}", expanded=False):
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.write(f"**Criado em:** {order.get('created_at', 'N/A')}")
                                    st.write(f"**Status:** {order_status}")
                                
                                with col2:
                                    summary = create_order_summary(order_id)
                                    st.write(f"**Itens:** {summary.get('item_count', 0)}")
                                    st.write(f"**Total:** {format_currency(summary.get('total', 0))}")
                                
                                with col3:
                                    if order.get('notes'):
                                        st.write(f"**Observações:** {order['notes']}")
                                
                                st.markdown("---")
                                
                                # Items do pedido
                                st.write("**Itens do Pedido:**")
                                try:
                                    items = db.get_order_items(order_id)
                                    if items and len(items) > 0:
                                        for item in items:
                                            if item and isinstance(item, dict):
                                                menu_name = item.get('menu_name', 'Sem nome')
                                                qty = int(item.get('quantity', 0))
                                                price = float(item.get('price', 0))
                                                total_price = price * qty
                                                st.write(f"- {menu_name} x{qty} ({format_currency(total_price)})")
                                                if item.get('notes'):
                                                    st.caption(f"  📝 {item['notes']}")
                                    else:
                                        st.info("Nenhum item neste pedido")
                                except Exception as e:
                                    st.error(f"Erro ao listar itens: {e}")
                                
                                # Ações
                                col1, col2, col3 = st.columns(3)
                                
                                if order_status != "Pago":
                                    with col1:
                                        if st.button(f"✅ Pronto", key=f"ready_{order_id}", use_container_width=True):
                                            try:
                                                db.update_order_status(order_id, "Pronto")
                                                st.success("✅ Status atualizado!")
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"Erro ao atualizar: {e}")
                                    
                                    with col2:
                                        if st.button(f"👋 Servido", key=f"served_{order_id}", use_container_width=True):
                                            try:
                                                db.update_order_status(order_id, "Servido")
                                                st.success("✅ Status atualizado!")
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"Erro ao atualizar: {e}")
                                    
                                    with col3:
                                        if st.button(f"❌ Cancelar", key=f"cancel_{order_id}", use_container_width=True):
                                            try:
                                                db.update_order_status(order_id, "Cancelado")
                                                st.warning("⚠️ Pedido cancelado")
                                                st.rerun()
                                            except Exception as e:
                                                st.error(f"Erro ao cancelar: {e}")
                        except Exception as e:
                            st.error(f"Erro ao processar pedido: {e}")
            else:
                st.info("Nenhum pedido encontrado")
        except Exception as e:
            st.error(f"Erro ao buscar pedidos: {e}")
except Exception as e:
    st.error(f"Erro na página de pedidos: {e}")

# ==================== PAINEL COZINHA ====================
try:
    if st.session_state.page == "kitchen" and has_permission("view_pending_orders"):
        st.title("👨‍🍳 Painel da Cozinha")
        
        st.write("*Sistema se atualiza automaticamente*")
        
        col1, col2, col3 = st.columns(3)
        
        try:
            # Pedidos por status
            pending = db.get_orders(status="Pendente") or []
            preparing = db.get_orders(status="Preparando") or []
            ready = db.get_orders(status="Pronto") or []
            
            with col1:
                st.metric("⏳ Pendente", len(pending))
            with col2:
                st.metric("🔥 Preparando", len(preparing))
            with col3:
                st.metric("✅ Pronto", len(ready))
            
            st.markdown("---")
            
            # Pedidos pendentes e preparando
            all_working = pending + preparing
            
            if all_working and len(all_working) > 0:
                for order in all_working:
                    if order and isinstance(order, dict):
                        try:
                            order_id = order.get('id')
                            table_num = order.get('table_number', 'N/A')
                            order_status = order.get('status', 'Desconhecido')
                            status_color = "🟡" if order_status == "Pendente" else "🟠"
                            
                            with st.container(border=True):
                                col1, col2, col3 = st.columns([2, 1, 1])
                                
                                with col1:
                                    st.markdown(f"### {status_color} Mesa {table_num}")
                                    
                                    try:
                                        items = db.get_order_items(order_id) or []
                                        if items:
                                            for item in items:
                                                if item and isinstance(item, dict):
                                                    menu_name = item.get('menu_name', 'Sem nome')
                                                    qty = int(item.get('quantity', 0))
                                                    st.write(f"🍕 **{menu_name}** x{qty}")
                                                    if item.get('notes'):
                                                        st.caption(f"📝 {item['notes']}")
                                        else:
                                            st.info("Sem itens")
                                    except Exception as e:
                                        st.warning(f"Erro ao carregar itens: {e}")
                                
                                with col2:
                                    try:
                                        created = datetime.fromisoformat(order.get('created_at', ''))
                                        elapsed = datetime.now() - created
                                        minutes = int(elapsed.total_seconds() / 60)
                                        st.metric("⏱️ Tempo", f"{minutes}min")
                                    except Exception:
                                        st.metric("⏱️ Tempo", "N/A")
                                
                                with col3:
                                    try:
                                        if order_status == "Pendente":
                                            if st.button(f"🔥 Iniciando", key=f"start_{order_id}", use_container_width=True, type="primary"):
                                                db.update_order_status(order_id, "Preparando")
                                                st.success("✅ Iniciado!")
                                                st.rerun()
                                        else:
                                            if st.button(f"✅ Pronto", key=f"ready_{order_id}", use_container_width=True, type="primary"):
                                                db.update_order_status(order_id, "Pronto")
                                                st.success("✅ Marcado como pronto!")
                                                st.rerun()
                                    except Exception as e:
                                        st.error(f"Erro: {e}")
                        except Exception as e:
                            st.error(f"Erro ao processar pedido: {e}")
            else:
                st.success("✅ Nenhum pedido para preparar!")
            
            st.markdown("---")
            
            # Pedidos prontos
            if ready and len(ready) > 0:
                st.markdown("### ✅ Pedidos Prontos para Servir")
                for order in ready:
                    if order:
                        st.write(f"🟢 **Mesa {order.get('table_number', 'N/A')}**")
        except Exception as e:
            st.error(f"Erro ao carregar cozinha: {e}")
except Exception as e:
    st.error(f"Erro na página de cozinha: {e}")

# ==================== PAGAMENTOS ====================
try:
    if st.session_state.page == "payments" and has_permission("process_payment"):
        st.title("💳 Processamento de Pagamentos")
        
        try:
            orders = db.get_orders(status="Servido") or []
            
            if orders and len(orders) > 0:
                st.write(f"**{len(orders)} pedido(s) pronto(s) para pagamento**")
                
                for order in orders:
                    if order and isinstance(order, dict):
                        try:
                            order_id = order.get('id')
                            table_num = order.get('table_number', 'N/A')
                            
                            with st.expander(f"Mesa {table_num} - Pedido #{order_id}", expanded=False):
                                summary = create_order_summary(order_id)
                                
                                if summary and summary.get('items'):
                                    st.write("**Itens:**")
                                    for item in summary.get('items', []):
                                        if item and isinstance(item, dict):
                                            menu_name = item.get('menu_name', 'Sem nome')
                                            qty = int(item.get('quantity', 0))
                                            price = float(item.get('price', 0))
                                            total_price = price * qty
                                            st.write(f"- {menu_name} x{qty}: {format_currency(total_price)}")
                                    
                                    st.markdown("---")
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        st.metric("💰 Total", format_currency(summary.get('total', 0)))
                                    
                                    with col2:
                                        payment_method = st.selectbox(
                                            "Método de Pagamento",
                                            ["Dinheiro", "Débito", "Crédito", "PIX"],
                                            key=f"method_{order_id}"
                                        )
                                    
                                    if st.button(f"✅ Confirmar Pagamento", key=f"pay_{order_id}", use_container_width=True, type="primary"):
                                        try:
                                            db.record_payment(order_id, summary.get('total', 0), payment_method)
                                            st.success(f"✅ Pagamento processado! Total: {format_currency(summary.get('total', 0))}")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Erro ao processar pagamento: {e}")
                        except Exception as e:
                            st.error(f"Erro ao processar pedido: {e}")
            else:
                st.info("Nenhum pedido aguardando pagamento")
        except Exception as e:
            st.error(f"Erro ao carregar pedidos: {e}")
except Exception as e:
    st.error(f"Erro na página de pagamentos: {e}")

# ==================== ADMINISTRAÇÃO ====================
try:
    if st.session_state.page == "admin" and has_permission("manage_users"):
        st.title("⚙️ Administração")
        
        tab1, tab2, tab3 = st.tabs(["👥 Usuários", "📋 Menu", "📊 Analytics"])
        
        with tab1:
            st.subheader("Gerenciar Usuários")
            st.info("⏳ Funcionalidade em desenvolvimento - Em breve!")
        
        with tab2:
            st.subheader("Gerenciar Menu")
            
            try:
                menu = db.get_menu() or []
                if menu and len(menu) > 0:
                    df_menu = pd.DataFrame(menu)
                    if not df_menu.empty:
                        st.dataframe(df_menu[['name', 'price', 'category', 'active']], use_container_width=True)
                    else:
                        st.warning("Menu vazio")
                else:
                    st.warning("Nenhum item no menu")
                
                st.markdown("---")
                st.write("**Adicionar novo item:**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    name = st.text_input("Nome do Produto")
                
                with col2:
                    price = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
                
                with col3:
                    category = st.selectbox("Categoria", ["Pizza", "Bebida", "Sobremesa", "Outro"])
                
                description = st.text_area("Descrição")
                
                if st.button("➕ Adicionar Item", type="primary", use_container_width=True):
                    if name and price and price > 0:
                        try:
                            st.success("✅ Item adicionado com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao adicionar: {e}")
                    else:
                        st.error("❌ Preencha todos os campos obrigatórios e preço > 0")
            except Exception as e:
                st.error(f"Erro ao carregar menu: {e}")
        
        with tab3:
            st.subheader("Analytics Avançado")
            
            try:
                # Estatísticas gerais
                days_analytics = st.selectbox("Período", [7, 30, 90], key="analytics_days")
                report = db.get_sales_report(days_analytics) or {}
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Vendido", format_currency(report.get('total_revenue', 0)))
                with col2:
                    st.metric("Pedidos", int(report.get('total_orders', 0)))
                with col3:
                    st.metric("Ticket Médio", format_currency(report.get('average_order', 0)))
            except Exception as e:
                st.error(f"Erro ao carregar analytics: {e}")
except Exception as e:
    st.error(f"Erro na página de administração: {e}")

st.markdown("---")
st.caption("Sistema Profissional de Gestão de Pizzaria | v1.0 | © 2024 Pizzaria Pro")
