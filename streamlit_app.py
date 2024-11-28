import streamlit as st
import pandas as pd
import os

# Nombre del archivo
file_name = "tesoro_curso.xlsx"

# Verificar si el archivo existe, sino crearlo
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=["Fecha", "Concepto", "Tipo de Movimiento", "Monto", "Saldo"])
    df.to_excel(file_name, index=False)

# Función para cargar datos
def cargar_datos():
    return pd.read_excel(file_name)

# Función para guardar datos
def guardar_datos(df):
    df.to_excel(file_name, index=False)

# Función para agregar un movimiento
def agregar_movimiento(fecha, concepto, tipo, monto):
    df = cargar_datos()
    saldo = df["Saldo"].iloc[-1] if not df.empty else 0
    nuevo_saldo = saldo + monto if tipo == "Entrada" else saldo - monto
    nuevo_movimiento = {"Fecha": fecha, "Concepto": concepto, "Tipo de Movimiento": tipo, "Monto": monto, "Saldo": nuevo_saldo}
    df = pd.concat([df, pd.DataFrame([nuevo_movimiento])], ignore_index=True)
    guardar_datos(df)
    return nuevo_saldo

# Interfaz de usuario
st.title("Gestión del Tesoro del Curso")

# Inputs del usuario
fecha = st.text_input("Fecha (DD/MM/AAAA):")
concepto = st.text_input("Concepto:")
tipo = st.selectbox("Tipo de Movimiento:", ["Entrada", "Salida"])
monto = st.number_input("Monto:", min_value=0.0)

if st.button("Agregar Movimiento"):
    if fecha and concepto:
        nuevo_saldo = agregar_movimiento(fecha, concepto, tipo, monto)
        st.success(f"Movimiento agregado. Saldo actual: {nuevo_saldo}")
    else:
        st.error("Completa todos los campos.")

if st.button("Descargar Reporte"):
    with open(file_name, "rb") as f:
        st.download_button("Descargar", f, file_name)
