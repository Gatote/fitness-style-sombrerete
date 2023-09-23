import pandas as pd
import mysql.connector
import streamlit as st




def consulta_deuda_clientes():
    try:
        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT client_id, concat(client_name, ' ', client_lastname), client_address, client_cellphone, balance  FROM client_debt")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()


resultados = consulta_deuda_clientes()

df = pd.DataFrame(resultados, columns = ["id","Nombre"," Dirección","Telefono celular","Balance (Deuda)"])

st.subheader('Balance de deudas de clientes',)
st.write("Listado de los clientes")
st.write("Un balance negativo se refiere a deuda del comercio al cliente")
st.dataframe(df, hide_index=1)