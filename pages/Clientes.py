import pandas as pd
import mysql.connector
import streamlit as st
import time
st.title("Clientes")

st.header("Clientes registrados")
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
        cursor.execute("SELECT *  FROM client")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

def query_client(name, lastname, colony, address, cellphone):
    try:
        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM client WHERE name = '{name}' AND lastname = '{lastname}' AND colony = '{colony}' AND address = '{address}' AND cellphone = '{cellphone}';")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

def add_new_client(name, lastname, colony, address, cellphone):
    try:
        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO client (name, lastname, colony, address, cellphone) VALUES ('{name}', '{lastname}',  '{colony}', '{address}', '{cellphone}')")
        conn.commit()
        st.success("Registro completado")
        time.sleep(1)
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()


resultados = consulta_deuda_clientes()

df_client = pd.DataFrame(resultados, columns = ["Id","Nombre","Apellido","Colonia","Dirección","Celular"])
st.write("Listado de los clientes")
st.dataframe(df_client, hide_index=1)

import re
def validar_entrada(texto):
    # Utiliza una expresión regular para permitir solo caracteres alfanuméricos y espacios
    return re.match("^[a-zA-Z0-9 ]*$", texto) is not None

with st.expander(label = "Agregar cliente", expanded = False):
    st.write("Llenar los siguientes datos para registrar al cliente")
    add_client_name = st.text_input(label = "Nombre", value = "", max_chars = 255, key = "add_client_name", help = "Nombre/s del cliente con el que se registrará en el sistema", placeholder = "Juan")
    add_client_lastname = st.text_input(label = "Apellido", value = "", max_chars = 255, key = "add_client_lastname", help = "Apellido/s del cliente con el que se registrará en el sistema", placeholder = "Ramirez", )
    add_client_colony = st.text_input(label = "Colonia", value = "", max_chars = 255, key = "add_client_colony", help = "Colonia/barrio en donde se encuentra la direccion del cliente", placeholder = "Sol")
    add_client_address = st.text_input(label = "Dirección", value = "", max_chars = 255, key = "add_client_address", help = "Dirección del cliente", placeholder = "Avenida Principal")
    add_client_cellphone = st.text_input(label = "Telefono de contacto", value = "", max_chars = 15, key = "add_client_cellphone", help = "Numero telefonico para contactar al cliente", placeholder = "(123) 456-7890")


    if add_client_name == "" or not validar_entrada(add_client_name):
        st.error("Se requiere un nombre válido y no vacio")
    elif add_client_lastname == "" or not validar_entrada(add_client_lastname):
        st.error("Se requiere un apellido válido y no vacio")
    elif add_client_cellphone == "":
        st.error("Se requiere un numero válido y no vacio")
    if query_client(add_client_name, add_client_lastname, add_client_colony, add_client_address, add_client_cellphone):
        st.info("Ya hay un registro idéntico")
    elif st.button(label = "Registrar cliente", key = "confirm_client_data", help = "Subir los datos al sistema"):
       add_new_client(add_client_name, add_client_lastname, add_client_colony, add_client_address, add_client_cellphone)

        





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
        cursor.execute("SELECT client_id, concat(client_name, ' ', client_lastname), client_cellphone, balance  FROM client_debt")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()


resultados = consulta_deuda_clientes()

df = pd.DataFrame(resultados, columns = ["id","Nombre completo","Telefono celular","Balance (Deuda)"])

st.subheader('Balance de deudas de clientes',)
st.write("Un balance negativo se refiere a deuda del comercio al cliente")
st.dataframe(df, hide_index=1)