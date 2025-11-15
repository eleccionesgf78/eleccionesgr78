import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Sorteo", page_icon="🎉")

st.title("🎉 SORTEO POR UNA NAVIDAD FELIZ")
st.write("Subí un archivo Excel con columnas **dni** y **nombre** para realizar el sorteo.")

archivo = st.file_uploader("Subir archivo Excel", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)

        # Validar si está vacío
        if df.empty:
            st.error("El archivo está vacío.")
            st.stop()

        # Validar columnas necesarias
        columnas = [c.lower() for c in df.columns]
        if "dni" not in columnas or "nombre" not in columnas:
            st.error("El archivo debe tener columnas 'dni' y 'nombre'.")
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
            st.success("No se encontraron DNIs duplicados.")

        st.write(f"Participantes válidos: {total_despues}")
        st.dataframe(df, use_container_width=True)

        # Parámetros del sorteo
        cant_ganadores = st.number_input(
            "Cantidad de ganadores", min_value=1, max_value=len(df), value=1
        )
        cant_suplentes = st.number_input(
            "Cantidad de suplentes",
            min_value=0,
            max_value=len(df) - cant_ganadores,
            value=0
        )

        # Sorteo
        if st.button("🎯 Realizar Sorteo"):
            participantes = df.sample(frac=1).reset_index(drop=True)  # shuffle seguro

            ganadores = participantes.iloc[:cant_ganadores]
            suplentes = participantes.iloc[cant_ganadores:cant_ganadores + cant_suplentes]

            st.subheader("🎉 Ganadores")
            st.table(ganadores)

            if not suplentes.empty:
                st.subheader("🟦 Suplentes")
                st.table(suplentes)

            # Si querés descargar resultados (opcional)
            #output = pd.ExcelWriter("resultado_sorteo.xlsx", engine="xlsxwriter")
            #ganadores.to_excel(output, sheet_name="Ganadores", index=False)
            #suplentes.to_excel(output, sheet_name="Suplentes", index=False)
            #output.save()
            #st.download_button("📥 Descargar resultados", data=open("resultado_sorteo.xlsx","rb"), file_name="sorteo.xlsx")

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

