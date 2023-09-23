import pandas as pd
import mysql.connector
import streamlit as st

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
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

# Obtener los resultados de la consulta
resultados = consulta_venta_diaria()

# Crear un DataFrame de Pandas con los resultados y establecer los encabezados
df = pd.DataFrame(resultados, columns=['id_venta', 'fecha', 'producto(cantidad)', 'compra', 'venta', 'ganancia', 'nombre_cliente'])

# Mostrar el DataFrame en Streamlit
st.subheader('Ventas del día')
st.dataframe(df, hide_index=1)
