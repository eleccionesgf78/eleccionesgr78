import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Sorteo", page_icon="🎉")

st.title("🎉 Sistema de Sorteo con Excel")
st.write("Subí un archivo Excel con columnas **dni** y **nombre** para realizar el sorteo.")

archivo = st.file_uploader("Subir archivo Excel", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)

        if "dni" not in df.columns or "nombre" not in df.columns:
            st.error("El archivo debe tener columnas 'dni' y 'nombre'.")
        else:
            st.success("Archivo cargado correctamente.")
            st.dataframe(df)

            cant_ganadores = st.number_input("Cantidad de ganadores", min_value=1, max_value=len(df), value=1)
            cant_suplentes = st.number_input("Cantidad de suplentes", min_value=0, max_value=len(df)-cant_ganadores, value=0)

            if st.button("🎯 Realizar Sorteo"):
                participantes = df.to_dict(orient="records")
                random.shuffle(participantes)

                ganadores = participantes[:cant_ganadores]
                suplentes = participantes[cant_ganadores:cant_ganadores+cant_suplentes]

                st.subheader("🎉 Ganadores")
                st.table(ganadores)

                if suplentes:
                    st.subheader("🟦 Suplentes")
                    st.table(suplentes)

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
