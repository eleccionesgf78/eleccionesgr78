import streamlit as st
import pandas as pd
import random
import time

# Configuración de la página
st.set_page_config(
    page_title="Sorteo Navideño", 
    page_icon="🎄",
    layout="centered"
)

# CSS minimalista con texto negro
st.markdown("""
<style>
    .stApp {
        background: white;
    }
    
    .main-header {
        text-align: center;
        color: #000000;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .mingo-header {
        text-align: center;
        color: #000000;
        font-size: 3rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .sub-header {
        text-align: center;
        color: #000000;
        font-size: 1.2rem;
        margin-top: 0;
    }
    
    .stButton button {
        background-color: #d63031;
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .stButton button:hover {
        background-color: #c23616;
        color: white;
    }
    
    .winner-section {
        background-color: #ffeaa7;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #d63031;
    }
    
    .suplente-section {
        background-color: #dfe6e9;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #0984e3;
    }
    
    /* Cambiar color de todos los textos de Streamlit a negro */
    .stMarkdown, .stHeader, .stSubheader, .stText, .stWrite {
        color: #000000 !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- ENCABEZADO ----------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:  # Columna central para la imagen
    st.image("LOGO_PJ_TERMAS.jpg", width=200, use_column_width=True)

# Títulos en negro
st.markdown('<p class="main-header">🎄 Sorteo Solidario por una Navidad Feliz 🎄</p>', unsafe_allow_html=True)
st.markdown('<p class="mingo-header">MINGO 2026</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sujeto a las bases y condiciones</p>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------- CARGA DE ARCHIVO ----------------------
st.markdown("<h2 style='color: #000000;'>📤 Subir archivo Excel</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #000000;'>Arrastra y suelta tu archivo Excel aquí</p>", unsafe_allow_html=True)

archivo = st.file_uploader(
    "Drag and drop file here",
    type=["xlsx"],
    help="Limit 200MB per file - XLSX",
    label_visibility="collapsed"
)

if archivo:
    try:
        # Cargar el archivo Excel
        df = pd.read_excel(archivo)
        
        # Mostrar información del archivo cargado
        st.success(f"✅ Archivo cargado correctamente")
        st.info(f"📊 Columnas detectadas: {list(df.columns)}")
        st.info(f"📝 Total de registros: {len(df)}")

        # Validar si está vacío
        if df.empty:
            st.error("❌ El archivo está vacío.")
            st.stop()

        # Buscar columnas que contengan "dni" y "nombre" (case insensitive)
        columnas = [str(col).lower().strip() for col in df.columns]
        
        # Encontrar nombres reales de las columnas
        columna_dni = None
        columna_nombre = None
        
        for col in df.columns:
            col_lower = str(col).lower().strip()
            if 'dni' in col_lower:
                columna_dni = col
            if 'nombre' in col_lower:
                columna_nombre = col

        # Validar que se encontraron las columnas necesarias
        if not columna_dni or not columna_nombre:
            st.error(f"❌ No se pudieron encontrar las columnas necesarias.")
            st.error(f"Columnas disponibles: {list(df.columns)}")
            st.error("El archivo debe tener una columna con 'DNI' y otra con 'Nombre'")
            st.stop()

        st.success(f"✅ Columnas identificadas: '{columna_dni}' y '{columna_nombre}'")

        # Crear un nuevo DataFrame solo con las columnas necesarias
        df_sorteo = df[[columna_dni, columna_nombre]].copy()
        
        # Renombrar columnas para consistencia
        df_sorteo.columns = ['dni', 'nombre']
        
        # Limpiar datos - eliminar filas con valores vacíos
        df_sorteo = df_sorteo.dropna()
        
        # Convertir DNI a string y limpiar
        df_sorteo['dni'] = df_sorteo['dni'].astype(str).str.strip()

        # ---- PRE-LIMPIEZA ----
        total_antes = len(df_sorteo)
        df_sorteo = df_sorteo.drop_duplicates(subset=["dni"], keep="first")
        total_despues = len(df_sorteo)
        eliminados = total_antes - total_despues

        if eliminados > 0:
            st.warning(f"⚠️ Se eliminaron {eliminados} participantes con DNI duplicado.")
        else:
            st.success("✅ No se encontraron DNIs duplicados.")

        st.markdown(f"<p style='color: #000000;'>🎅 Participantes válidos para el sorteo: <strong>{total_despues}</strong></p>", unsafe_allow_html=True)
        
        with st.expander("📋 Ver lista completa de participantes"):
            st.dataframe(df_sorteo, use_container_width=True)

        # Parámetros del sorteo
        col1, col2 = st.columns(2)
        
        with col1:
            cant_ganadores = st.number_input(
                "🎁 Cantidad de ganadores", 
                min_value=1, 
                max_value=len(df_sorteo), 
                value=1,
                help="Número de ganadores principales"
            )
        
        with col2:
            cant_suplentes = st.number_input(
                "🟦 Cantidad de suplentes",
                min_value=0,
                max_value=len(df_sorteo) - cant_ganadores,
                value=0,
                help="Ganadores suplentes en caso de que los principales no puedan recibir el premio"
            )

        # Sorteo
        if st.button("🎯 Realizar Sorteo", use_container_width=True):
            
            # Contador regresivo con suspenso
            countdown_placeholder = st.empty()
            for i in range(3, 0, -1):
                countdown_placeholder.markdown(f"<h1 style='text-align: center; color: #000000;'>🎄 {i} 🎄</h1>", unsafe_allow_html=True)
                time.sleep(1)
            
            countdown_placeholder.markdown("<h1 style='text-align: center; color: #000000;'>🎉 ¡SORTEANDO! 🎉</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
            # Animación de mezcla con progreso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                status_text.text(f"Mezclando participantes... {i+1}%")
                time.sleep(0.02)
            
            status_text.text("✅ ¡Mezcla completada!")
            time.sleep(0.5)

            # Realizar el sorteo
            participantes = df_sorteo.sample(frac=1).reset_index(drop=True)
            ganadores = participantes.iloc[:cant_ganadores]
            suplentes = participantes.iloc[cant_ganadores:cant_ganadores + cant_suplentes]

            # Limpiar elementos de animación
            progress_bar.empty()
            status_text.empty()
            countdown_placeholder.empty()

            # Mostrar resultados
            st.balloons()
            
            st.markdown("---")
            st.markdown('<div class="winner-section">', unsafe_allow_html=True)
            st.markdown("<h3 style='color: #000000;'>🎉 ¡GANADORES OFICIALES! 🎉</h3>", unsafe_allow_html=True)
            
            # Mostrar ganadores uno por uno
            for idx, (_, ganador) in enumerate(ganadores.iterrows(), 1):
                with st.container():
                    col_a, col_b = st.columns([1, 3])
                    with col_a:
                        st.metric(f"Ganador {idx}", "🎁")
                    with col_b:
                        st.markdown(f"<p style='color: #000000;'><strong>Nombre:</strong> {ganador['nombre']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #000000;'><strong>DNI:</strong> {ganador['dni']}</p>", unsafe_allow_html=True)
                if idx < len(ganadores):
                    st.write("---")
            
            st.markdown('</div>', unsafe_allow_html=True)

            if not suplentes.empty:
                st.markdown('<div class="suplente-section">', unsafe_allow_html=True)
                st.markdown("<h3 style='color: #000000;'>🟦 LISTA DE SUPLENTES</h3>", unsafe_allow_html=True)
                st.table(suplentes)
                st.markdown('</div>', unsafe_allow_html=True)
                
            st.success("🎊 ¡Sorteo completado exitosamente! 🎊")
            
            # Botón para reiniciar
            if st.button("🔄 Realizar otro sorteo", use_container_width=True):
                st.rerun()

    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
        st.error("Por favor, verifica que el archivo sea un Excel válido.")

# Footer simple en negro
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #000000;'>🎅 ¡Felices Fiestas! 🎄</p>", 
    unsafe_allow_html=True
)
