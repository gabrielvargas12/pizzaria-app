# PEDIDOS

if menu=="🍕 NOVO PEDIDO":

    st.title("🍕 Novo Pedido")

    if "pizza_escolhida" not in st.session_state:
        st.session_state.pizza_escolhida=None

    st.subheader(
        "Escolha a Pizza"
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

        for c,sabor in zip(
            cols,
            grupo
        ):

            if c.button(
                sabor,
                use_container_width=True
            ):

                st.session_state.pizza_escolhida=sabor

    if st.session_state.pizza_escolhida:

        st.divider()

        st.success(
f"""
🍕 Selecionada:
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
