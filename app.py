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

# CSS personalizado para tema navideño con fondo
st.markdown("""
<style>
    .stApp {
        background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), 
                          url('https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .main-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 2px solid #d63031;
    }
    
    .main-header {
        text-align: center;
        color: #d63031;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #2d3436;
        font-size: 1.2rem;
        margin-top: 0;
    }
    
    .stButton button {
        background: linear-gradient(45deg, #d63031, #e17055);
        color: white;
        border: none;
        padding: 0.8rem 2.5rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(214, 48, 49, 0.4);
    }
    
    .winner-section {
        background: linear-gradient(135deg, #ffeaa7, #fab1a0);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 8px solid #d63031;
        animation: pulse 2s infinite;
    }
    
    .suplente-section {
        background: linear-gradient(135deg, #dfe6e9, #b2bec3);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 8px solid #0984e3;
    }
    
    .countdown {
        font-size: 3rem;
        text-align: center;
        color: #d63031;
        font-weight: bold;
        animation: bounce 1s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(214, 48, 49, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(214, 48, 49, 0); }
        100% { box-shadow: 0 0 0 0 rgba(214, 48, 49, 0); }
    }
    
    .snowflake {
        position: fixed;
        top: -10px;
        color: #74b9ff;
        font-size: 20px;
        animation: fall linear forwards;
        z-index: -1;
    }
    
    @keyframes fall {
        to { transform: translateY(100vh) rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Función para crear efecto de nieve (CORREGIDA)
def add_snow_effect():
    snow_html = "<div id='snow-container'>"
    for _ in range(30):
        left_pos = random.randint(1, 100)
        duration = random.uniform(5, 15)
        delay = random.uniform(0, 5)
        snow_html += f'<div class="snowflake" style="left: {left_pos}%; animation-duration: {duration}s; animation-delay: {delay}s;">❄️</div>'
    snow_html += "</div>"
    st.markdown(snow_html, unsafe_allow_html=True)

# Añadir efecto de nieve
add_snow_effect()

# Contenedor principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ---------------------- ENCABEZADO MEJORADO ----------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:  # Columna central para la imagen
    st.image("LOGO_PJ_TERMAS.jpg", width=200, use_column_width=True)

# Título centrado y sin guiones
st.markdown('<p class="main-header">🎄 Sorteo Solidario por una Navidad Feliz 🎄</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">MINGO 2026</p>', unsafe_allow_html=True)
st.caption("Sujeto a las bases y condiciones")

st.markdown("---")

# ---------------------- CARGA DE ARCHIVO ----------------------
st.header("📤 Subir archivo Excel")
archivo = st.file_uploader(
    "Arrastra y suelta tu archivo aquí", 
    type=["xlsx"],
    help="Formatos aceptados: .xlsx (Máximo 200MB)"
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

        st.info(f"🎅 Participantes válidos para el sorteo: **{total_despues}**")
        
        with st.expander("📋 Ver lista completa de participantes"):
            st.dataframe(df, use_container_width=True)

        # Parámetros del sorteo
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
            st.subheader("🎉 ¡GANADORES OFICIALES! 🎉")
            
            # Mostrar ganadores uno por uno con animación
            for idx, (_, ganador) in enumerate(ganadores.iterrows(), 1):
                with st.container():
                    col_a, col_b = st.columns([1, 3])
                    with col_a:
                        st.metric(f"Ganador {idx}", "🎁")
                    with col_b:
                        st.write(f"**Nombre:** {ganador['nombre']}")
                        st.write(f"**DNI:** {ganador['dni']}")
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
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #636e72; padding: 2rem;'>
        <h3 style='color: #d63031;'>🎅 ¡Felices Fiestas! 🎄</h3>
        <p>Que la magia de la Navidad llene sus hogares de alegría y esperanza</p>
    </div>
    """, 
    unsafe_allow_html=True
)
