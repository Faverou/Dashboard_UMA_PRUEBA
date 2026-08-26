import pandas as pd
import streamlit as st

# Configuración general de la página
st.set_page_config(
    page_title="Dashboard Consolidado UMA",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Dashboard: Programación en Curso y Consolidado UMA")
st.markdown("---")

# Ruta del archivo Excel proporcionado
excel_file = "Programación en curso y consolidado UMA (1)_2.xlsx"

@st.cache_data
def cargar_datos(file):
    # Identificar las hojas disponibles en el libro de Excel
    xls = pd.ExcelFile(file)
    sheet_names = xls.sheet_names
    return xls, sheet_names

try:
    xls, sheet_names = cargar_datos(excel_file)
    
    # Selector de hoja en la barra lateral
    st.sidebar.header("Configuración de Visualización")
    selected_sheet = st.sidebar.selectbox("Selecciona la hoja del consolidado", sheet_names)
    
    # Cargar la hoja seleccionada
    df = pd.read_excel(excel_file, sheet_name=selected_sheet)
    
    # Mostrar resumen de la hoja activa
    st.subheader(bahía_titulo := f"Vista General: {selected_sheet}")
    
    # Métricas principales (KPIs de ejemplo basados en la estructura general)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total de Registros", value=len(df))
    with col2:
        st.metric(label="Columnas Analizadas", value=len(df.columns))
    with col3:
        if 'Estado' in df.columns:
            activos = len(df[df['Estado'].astype(str).str.contains('Curso|Pendiente', case=False, na=False)])
            st.metric(label="En Curso / Pendientes", value=activos)
        else:
            st.metric(label="Variables de Control", value="N/D")
    with col4:
        st.metric(label="Hojas en el Libro", value=len(sheet_names))

    st.markdown("---")
    
    # Filtros interactivos opcionales si existen columnas de texto relevantes
    st.subheader("Filtros y Detalle de Datos")
    
    # Mostrar la tabla de datos interactiva
    st.dataframe(df, use_container_width=True)
    
    # Sección de análisis visual básico
    if len(df.select_dtypes(include=['number']).columns) > 0:
        st.markdown("---")
        st.subheader("Análisis Gráfico Rápido")
        num_col = st.selectbox("Selecciona una métrica numérica para graficar", df.select_dtypes(include=['number']).columns)
        st.bar_chart(df[num_col].head(25))

except Exception as e:
    st.error(f"Se produjo un error al cargar o procesar el archivo: {e}")
    st.info("Por favor, asegúrate de que el archivo Excel esté en la misma ruta y no esté abierto en otra aplicación.")