import streamlit as st
from carrito_imperativo import cargar_catalogo, armar_carrito_imperativo, calcular_total
from carrito_poo import ejecutar_poo
from carrito_funcional import ejecutar_funcional

st.set_page_config(page_title="Sbeaty - Arma tu Rutina", page_icon="✨", layout="centered")

st.title("✨ Sbeaty | Arma tu Rutina Ideal")
st.write("Selecciona tu **tipo de piel** y tu **presupuesto** para armar tu carrito personalizado.")

catalogo = cargar_catalogo("productos.json")

col1, col2 = st.columns(2)
with col1:
    tipo_piel = st.selectbox("1. ¿Cuál es tu tipo de piel?", ["grasa", "mixta", "seca", "sensible"])
with col2:
    presupuesto = st.number_input("2. Presupuesto máximo (CLP)", min_value=5000, max_value=200000, value=30000, step=1000)

paradigma = st.radio(
    "Motor de cálculo (3 paradigmas solicitados en la pauta):",
    ["Imperativo", "Orientado a Objetos (POO)", "Funcional"],
    horizontal=True,
)

if st.button("🛍️ Armar mi rutina ahora", type="primary"):
    if paradigma == "Imperativo":
        items, _ = armar_carrito_imperativo(catalogo, tipo_piel, presupuesto)
    elif paradigma == "Orientado a Objetos (POO)":
        items, _ = ejecutar_poo("productos.json", tipo_piel, presupuesto)
    else:
        items, _ = ejecutar_funcional("productos.json", tipo_piel, presupuesto)

    st.session_state["carrito"] = items
    st.session_state["piel"] = tipo_piel
    st.session_state["presupuesto"] = presupuesto

if "carrito" in st.session_state:
    st.divider()
    st.subheader("Tu Carrito Evento Especial (Modalidad Automática e Interactiva)")
    carrito = st.session_state["carrito"]

    if not carrito:
        st.warning("No alcanzaron productos con ese presupuesto. Sube un poco el monto.")
    else:
        for i, prod in enumerate(carrito):
            c1, c2, c3 = st.columns([4, 2, 1])
            c1.write(f"**{prod['nombre']}** ({prod['categoria']})")
            c2.write(f"${prod['precio']:,} CLP".replace(",", "."))
            if c3.button("Quitar", key=f"del_{prod['id']}_{i}"):
                carrito.pop(i)
                st.session_state["carrito"] = carrito
                st.rerun()

        total = calcular_total(carrito)
        restante = st.session_state["presupuesto"] - total
        st.success(f"**Total carrito:** ${total:,} CLP  |  **Saldo disponible:** ${restante:,} CLP".replace(",", "."))

        ids_actuales = {p["id"] for p in carrito}
        agregables = [
            p for p in catalogo
            if st.session_state["piel"] in p["pieles"]
            and p["id"] not in ids_actuales
            and p["precio"] <= restante
        ]

        if agregables:
            st.write("**¿Quieres agregar otro producto compatible con lo que te sobra?**")
            opciones = {f"{p['nombre']} (${p['precio']:,})": p for p in agregables}
            elegido_txt = st.selectbox("Productos disponibles:", list(opciones.keys()))
            if st.button("➕ Agregar al carrito"):
                carrito.append(opciones[elegido_txt])
                st.session_state["carrito"] = carrito
                st.rerun()