# 🐔 Análisis Financiero del Ciclo de Engorde de Pollos

Esta es una aplicación interactiva desarrollada con Streamlit que permite a los usuarios analizar la viabilidad financiera de un ciclo de engorde de pollos. Ofrece una herramienta sencilla para calcular costos, ingresos y ganancia neta, permitiendo la modificación de parámetros clave en tiempo real y la descarga de un informe completo.

## 🚀 Características

* **Parámetros Ajustables:** Modifica fácilmente el número de pollos, precios de compra y venta, costos de alimento, costos de sacrificio, tasa de mortalidad y un gasto extra por eventualidades.
* **Cálculos en Tiempo Real:** Visualiza instantáneamente los ingresos totales, costos totales y la ganancia neta a medida que ajustas los parámetros.
* **Resumen Financiero Detallado:** Una tabla clara que desglosa todos los componentes de costo y beneficio.
* **Visualización de Datos:** Gráfico de barras comparando ingresos y costos para una rápida comprensión del rendimiento.
* **Descarga de Informe en Excel:** Exporta un archivo Excel que incluye el resumen financiero y los parámetros de entrada utilizados para el análisis.

## 🛠️ Cómo Usar (Localmente)

Para ejecutar esta aplicación en tu máquina local, sigue estos pasos:

### 1. Clona el Repositorio (si ya lo tienes en GitHub)

```bash
git clone https://github.com/Diegocelsia/An-lisis-Financiero-del-Ciclo-de-Engorde-de-Pollos.git
cd analisis-pollos-streamlit
```



#### 2. Crea un Entorno Virtual (Recomendado)

```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

#### 3. Instala las Dependencias
```bash
pip install -r requirements.txt
```

#### 4. Ejecuta la Aplicación Streamlit
```bash
streamlit run app_pollos.py
```