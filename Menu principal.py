import pandas as pd
import mysql.connector
import streamlit as st
# Configurar la página de Streamlit
st.set_page_config(
    page_title="FITNESS STYLE SOMBRERETE",
    layout="wide",  # Cambiar el diseño a "wide" para aprovechar más espacio horizontal
    initial_sidebar_state="collapsed",  # Colapsar la barra lateral inicialmente
)


def consulta_venta_diaria():
    try:
        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        # Crear un cursor para ejecutar comandos en la base de datos
        cursor = conn.cursor()
        # Ejecutar una consulta SQL real para seleccionar datos de una tabla
        cursor.execute("SELECT * FROM sales_info_daily")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    except Exception as e:
        st.info(f"No hay conexion al servidor")

st.title(body = "Fitness Style Sombrerete   ")


# Obtener los resultados de la consulta
resultados = consulta_venta_diaria()

# Crear un DataFrame de Pandas con los resultados y establecer los encabezados
df = pd.DataFrame(resultados, columns=['id_venta', 'fecha', 'producto(cantidad)', 'compra', 'venta', 'ganancia', 'nombre_cliente'])

# Mostrar el DataFrame en Streamlit
st.subheader('Ventas del día')
st.dataframe(df, hide_index=1)
