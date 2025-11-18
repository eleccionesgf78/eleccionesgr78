import streamlit as st
import pandas as pd
import random
import time

# Configuración de la página con tema navideño
st.set_page_config(
    page_title="Sorteo Navideño", 
    page_icon="🎄",
    layout="centered"
)

# CSS personalizado para tema navideño con fondo mejorado
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .main-container {
        background-color: rgba(255, 255, 255, 0.98);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        border: 3px solid #d63031;
        margin: 2rem auto;
        max-width: 900px;
    }
    
    .main-header {
        text-align: center;
        color: #d63031;
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .mingo-header {
        text-align: center;
        color: #1e3c72;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .sub-header {
        text-align: center;
        color: #2d3436;
        font-size: 1.3rem;
        margin-top: 0;
        font-weight: 500;
    }
    
    .stButton button {
        background: linear-gradient(45deg, #d63031, #e17055);
        color: white;
        border: none;
        padding: 1rem 3rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(214, 48, 49, 0.4);
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #d63031;
        margin: 2rem 0;
    }
    
    .winner-section {
        background: linear-gradient(135deg, #ffeaa7, #fab1a0);
        padding: 2rem;
        border-radius: 15px;
        border-left: 10px solid #d63031;
        animation: pulse 2s infinite;
        margin: 1rem 0;
    }
    
    .suplente-section {
        background: linear-gradient(135deg, #dfe6e9, #b2bec3);
        padding: 2rem;
        border-radius: 15px;
        border-left: 10px solid #0984e3;
        margin: 1rem 0;
    }
    
    .countdown {
        font-size: 4rem;
        text-align: center;
        color: #d63031;
        font-weight: bold;
        animation: bounce 1s infinite;
        margin: 2rem 0;
    }
    
    .participant-count {
        font-size: 1.4rem;
        font-weight: bold;
        color: #1e3c72;
        text-align: center;
        margin: 1rem 0;
    }
    
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(214, 48, 49, 0.4); }
        70% { box-shadow: 0 0 0 20px rgba(214, 48, 49, 0); }
        100% { box-shadow: 0 0 0 0 rgba(214, 48, 49, 0); }
    }
    
    .file-uploader {
        background-color: white;
        border: 2px dashed #d63031 !important;
        border-radius: 10px;
        padding: 2rem;
    }
    
    .footer {
        text-align: center;
        color: white;
        padding: 2rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Contenedor principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ---------------------- ENCABEZADO MEJORADO ----------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:  # Columna central para la imagen
    st.image("LOGO_PJ_TERMAS.jpg", width=220, use_column_width=True)

# Títulos con mejor jerarquía y MINGO más grande
st.markdown('<p class="main-header">🎄 Sorteo Solidario por una Navidad Feliz 🎄</p>', unsafe_allow_html=True)
st.markdown('<p class="mingo-header">MINGO 2026</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sujeto a las bases y condiciones</p>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------- CARGA DE ARCHIVO MEJORADA ----------------------
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h2 style='color: #1e3c72;'>📤 Subir archivo Excel</h2>
    <p style='color: #636e72; font-size: 1.1rem;'>Arrastra y suelta tu archivo Excel aquí</p>
</div>
""", unsafe_allow_html=True)

archivo = st.file_uploader(
    " ",
    type=["xlsx"],
    help="Formatos aceptados: .xlsx (Máximo 200MB)",
    label_visibility="collapsed"
)

if archivo:
    try:
        df = pd.read_excel(archivo)

        # Validar si está vacío
        if df.empty:
            st.error("❌ El archivo está vacío.")
            st.stop()

        # Validar columnas necesarias
        columnas = [c.lower() for c in df.columns]
        if "dni" not in columnas or "nombre" not in columnas:
            st.error("❌ El archivo debe tener columnas 'DNI' y 'Nombre'.")
            st.stop()

        # Normalizar nombres de columnas
        df.columns = [c.lower() for c in df.columns]

        # ---- PRE-LIMPIEZA ----
        total_antes = len(df)
        df = df.drop_duplicates(subset=["dni"], keep="first")
        total_despues = len(df)
        eliminados = total_antes - total_despues

        if eliminados > 0:
            st.warning(f"⚠️ Se eliminaron {eliminados} participantes con DNI duplicado.")
        else:
            st.success("✅ No se encontraron DNIs duplicados.")

        st.markdown(f'<div class="participant-count">🎅 Participantes válidos para el sorteo: {total_despues}</div>', unsafe_allow_html=True)
        
        with st.expander("📋 Ver lista completa de participantes", expanded=False):
            st.dataframe(df, use_container_width=True)

        # Parámetros del sorteo
        st.markdown("---")
        st.subheader("🎯 Configuración del Sorteo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cant_ganadores = st.number_input(
                "🎁 Cantidad de ganadores", 
                min_value=1, 
                max_value=len(df), 
                value=1,
                help="Número de ganadores principales"
            )
        
        with col2:
            cant_suplentes = st.number_input(
                "🟦 Cantidad de suplentes",
                min_value=0,
                max_value=len(df) - cant_ganadores,
                value=0,
                help="Ganadores suplentes en caso de que los principales no puedan recibir el premio"
            )

        # Sorteo con suspenso
        if st.button("🎯 Realizar Sorteo con Suspenso", use_container_width=True):
            
            # Contador regresivo con suspenso
            countdown_placeholder = st.empty()
            for i in range(3, 0, -1):
                countdown_placeholder.markdown(f'<div class="countdown">🎄 {i} 🎄</div>', unsafe_allow_html=True)
                time.sleep(1)
            
            countdown_placeholder.markdown('<div class="countdown">🎉 ¡SORTEANDO! 🎉</div>', unsafe_allow_html=True)
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
            participantes = df.sample(frac=1).reset_index(drop=True)
            ganadores = participantes.iloc[:cant_ganadores]
            suplentes = participantes.iloc[cant_ganadores:cant_ganadores + cant_suplentes]

            # Limpiar elementos de animación
            progress_bar.empty()
            status_text.empty()
            countdown_placeholder.empty()

            # Mostrar resultados con estilo navideño
            st.balloons()
            
            st.markdown("---")
            st.markdown('<div class="winner-section">', unsafe_allow_html=True)
            st.markdown('<h2 style="text-align: center; color: #d63031;">🎉 ¡GANADORES OFICIALES! 🎉</h2>', unsafe_allow_html=True)
            
            # Mostrar ganadores uno por uno con animación
            for idx, (_, ganador) in enumerate(ganadores.iterrows(), 1):
                with st.container():
                    col_a, col_b = st.columns([1, 3])
                    with col_a:
                        st.metric(f"Ganador {idx}", "🎁")
                    with col_b:
                        st.write(f"**Nombre:** {ganador['nombre']}")
                        st.write(f"**DNI:** {ganador['dni']}")
                if idx < len(ganadores):
                    st.write("---")
            
            st.markdown('</div>', unsafe_allow_html=True)

            if not suplentes.empty:
                st.markdown('<div class="suplente-section">', unsafe_allow_html=True)
                st.subheader("🟦 LISTA DE SUPLENTES")
                st.table(suplentes)
                st.markdown('</div>', unsafe_allow_html=True)
                
            # Efectos de confeti adicional
            st.success("🎊 ¡Sorteo completado exitosamente! 🎊")
            
            # Botón para reiniciar
            if st.button("🔄 Realizar otro sorteo", use_container_width=True):
                st.rerun()

    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Footer navideño mejorado
st.markdown("""
<div class="footer">
    <h3 style='color: white;'>🎅 ¡Felices Fiestas! 🎄</h3>
    <p style='color: white; font-size: 1.1rem;'>Que la magia de la Navidad llene sus hogares de alegría y esperanza</p>
    <p style='color: white; font-size: 1rem; margin-top: 1rem;'><strong>MINGO 2026</strong> - Haciendo posible la magia navideña</p>
</div>
""", unsafe_allow_html=True)
