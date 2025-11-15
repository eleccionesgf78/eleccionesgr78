import streamlit as st
import pandas as pd
import random

# Configuración
st.set_page_config(page_title="Sorteo", page_icon="🎉")

# Mostrar el LOGO arriba del título
st.image("LOGO_PJ_TERMAS.jpg", width=350)  # ajustá el tamaño si querés

st.title("Sistema de Sorteo con Excel (sin duplicados)")
st.write("Subí un archivo Excel con columnas **dni** y **nombre** para realizar el sorteo.")

# Subir archivo
uploaded_file = st.file_uploader("Subir archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Validación de columnas
    if "dni" not in df.columns or "nombre" not in df.columns:
        st.error("El archivo debe tener columnas: dni y nombre.")
    else:
        # Eliminar duplicados por DNI
        df = df.drop_duplicates(subset="dni")

        st.write("### Vista previa de los datos:")
        st.dataframe(df)

        # Cantidad de ganadores
        cantidad = st.number_input("Cantidad de ganadores", min_value=1, max_value=len(df), step=1)

        if st.button("Realizar sorteo"):
            ganadores = df.sample(n=cantidad)
            st.success("🎉 ¡Sorteo realizado!")
            st.write("### Ganadores:")
            st.dataframe(ganadores)

            # Descargar resultados
            ganadores_excel = ganadores.to_excel(index=False)
            st.download_button(
                label="Descargar ganadores",
                data=ganadores.to_csv(index=False).encode("utf-8"),
                file_name="ganadores.csv",
                mime="text/csv",
            )
