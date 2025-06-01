import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# --- Configuración de la página ---
st.set_page_config(
    page_title="Análisis de Engorde de Pollos",
    page_icon="🐔",
    layout="wide"
)

st.title("🐔 Análisis Financiero del Ciclo de Engorde de Pollos")

# --- 1. Parámetros de Entrada ---
st.header("1. Parámetros de Entrada")

col_input1, col_input2 = st.columns(2)

with col_input1:
    pollos_comprados = st.number_input(
        "Número de pollos comprados",
        min_value=1,
        value=50,
        step=5,
        help="Cantidad inicial de pollos."
    )
    precio_pollos = st.number_input(
        "Precio por pollo (COP)",
        min_value=1000,
        value=4000,
        step=500,
        help="Costo individual de cada pollo."
    )
    bultos_alimento = st.number_input(
        "Bultos de alimento",
        min_value=1,
        value=6,
        step=1,
        help="Cantidad de bultos de alimento consumidos."
    )
    costo_bulto = st.number_input(
        "Costo por bulto de alimento (COP)",
        min_value=10000,
        value=108000,
        step=10000,
        help="Costo de un bulto de alimento."
    )


with col_input2:
    peso_promedio_libras = st.number_input(
        "Peso promedio por pollo (lbs)",
        min_value=1.0,
        value=6.25,
        step=0.25,
        format="%.2f",
        help="Peso promedio de cada pollo al momento de la venta."
    )
    precio_libra = st.number_input(
        "Precio por libra (COP)",
        min_value=1000,
        value=6500,
        step=500,
        help="Precio de venta por libra de carne de pollo."
    )
    tasa_mortalidad = st.slider(
        "Tasa de mortalidad (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.5,
        help="Porcentaje de pollos que se pierden (enfermedad, etc.)."
    ) / 100 # Dividir por 100 para convertir a decimal

    sacrificio_por_pollo = st.number_input(
        "Costo sacrificio/pollo (COP)",
        min_value=0,
        value=1500,
        step=100,
        help="Costo asociado al proceso de sacrificio por cada pollo."
    )
    gasto_extra = st.number_input(
        "Gasto Extra / Eventualidad (COP)",
        min_value=0,
        value=0,
        step=10000,
        help="Costo adicional no contemplado inicialmente (ej. medicinas extras)."
    )


# --- 2. Cálculos y Resultados ---
st.header("2. Cálculos y Resultados")

pollos_vendidos = int(pollos_comprados * (1 - tasa_mortalidad))
total_libras = pollos_vendidos * peso_promedio_libras
ingresos_totales = total_libras * precio_libra

costo_pollos = pollos_comprados * precio_pollos
costo_alimento = bultos_alimento * costo_bulto
costo_sacrificio = pollos_vendidos * sacrificio_por_pollo
costo_total = costo_pollos + costo_alimento + costo_sacrificio + gasto_extra
ganancia_neta = ingresos_totales - costo_total

# Mostrar métricas clave en una sola fila
col_metrics_1, col_metrics_2, col_metrics_3, col_metrics_4 = st.columns(4)

with col_metrics_1:
    st.metric("Pollos Vendidos", f"{pollos_vendidos} u.")
with col_metrics_2:
    st.metric("Libras Vendidas", f"{total_libras:,.2f} lbs")
with col_metrics_3:
    st.metric("Ingresos Totales", f"${ingresos_totales:,.0f} COP")
with col_metrics_4:
    st.metric("Costo Total", f"${costo_total:,.0f} COP")

# Mostrar Ganancia Neta con color condicional
if ganancia_neta >= 0:
    st.markdown(f"### Ganancia Neta: <span style='color:green'>${ganancia_neta:,.0f} COP</span>", unsafe_allow_html=True)
else:
    st.markdown(f"### Ganancia Neta: <span style='color:red'>${ganancia_neta:,.0f} COP</span>", unsafe_allow_html=True)


# --- 3. Resumen Financiero y Visualización ---
# Usamos dos columnas para la tabla y el gráfico para que estén uno al lado del otro
col_summary, col_chart = st.columns([1, 1.5]) # Damos más espacio al gráfico

with col_summary:
    st.subheader("Resumen Financiero")
    df = pd.DataFrame({
        "Concepto": [
            "Compra de pollos", "Alimento", "Sacrificio", "Gasto Extra",
            "Total Costos", "Ingresos por venta", "Ganancia neta"
        ],
        "Valor (COP)": [
            costo_pollos, costo_alimento, costo_sacrificio, gasto_extra,
            costo_total, ingresos_totales, ganancia_neta
        ]
    })
    st.dataframe(df.style.format({"Valor (COP)": "COP {:,}"}), height=230)

    # --- Descargar Excel ---
    st.subheader("Descargar Resultados")

    params_df = pd.DataFrame({
        "Parámetro": [
            "Pollos Comprados", "Precio por Pollo (COP)", "Bultos de Alimento",
            "Costo por Bulto (COP)", "Peso Promedio por Pollo (lbs)",
            "Precio por Libra (COP)", "Tasa de Mortalidad (%)",
            "Costo Sacrificio por Pollo (COP)", "Gasto Extra / Eventualidad (COP)"
        ],
        "Valor": [
            pollos_comprados, precio_pollos, bultos_alimento, costo_bulto,
            peso_promedio_libras, precio_libra, tasa_mortalidad * 100,
            sacrificio_por_pollo, gasto_extra
        ]
    })

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resumen Financiero')
        params_df.to_excel(writer, index=False, sheet_name='Parametros de Entrada')
    output.seek(0)

    st.download_button(
        label="Descargar Informe Completo (Excel)",
        data=output.getvalue(),
        file_name="informe_pollos_engorde.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_chart:
    st.subheader("Visualización de Ingresos vs Costos")
    # AÚN MÁS PEQUEÑO: ajustando el figsize
    fig, ax = plt.subplots(figsize=(6.1, 3.2)) # Reducido ligeramente (de 6.8, 3.8 a 6.5, 3.6)
    sns.barplot(data=df[df["Concepto"].isin(["Total Costos", "Ingresos por venta"])],
                x="Concepto", y="Valor (COP)", hue="Concepto", legend=False,
                palette=["#ff9999", "#99ff99"], ax=ax)
    plt.title("Ingresos vs Costos", fontsize=12) # Título un poco más pequeño
    plt.ylabel("Valor (COP)", fontsize=8) # Etiqueta más pequeña
    plt.xlabel("")
    plt.ticklabel_format(style='plain', axis='y')
    plt.xticks(fontsize=8) # Ajusta tamaño de etiquetas del eje X
    plt.yticks(fontsize=8) # Ajusta tamaño de etiquetas del eje Y


    # Añadir valores sobre las barras
    for p in ax.patches:
        ax.annotate(f'${p.get_height():,.0f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 2), # Ajuste para que el texto esté más cerca de la barra
                    textcoords='offset points',
                    fontsize=7, # Tamaño de fuente más pequeño para los valores
                    color='black')

    plt.tight_layout()
    st.pyplot(fig)

st.markdown("""
    ---
    *Desarrollado con Streamlit por Diego*
""")