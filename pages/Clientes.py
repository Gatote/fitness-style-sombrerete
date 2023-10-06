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

def validate_client(name, lastname, colony, address, cellphone):
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

df_client = pd.DataFrame(resultados, columns = ["Id","Nombre","Apellido","Colonia","Dirección","Celular","Deuda","Comenterios"])
st.write("Listado de los clientes")

if len(df_client) > 5:
    st.dataframe(df_client, hide_index=1, height = 248)
else:
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

    if validate_client(add_client_name, add_client_lastname, add_client_colony, add_client_address, add_client_cellphone):
        st.info("Ya hay un registro idéntico")

    if add_client_name == "" or not validar_entrada(add_client_name):
        st.error("Se requiere un nombre válido y no vacio")
    elif add_client_lastname == "" or not validar_entrada(add_client_lastname):
        st.error("Se requiere un apellido válido y no vacio")
    elif add_client_cellphone == "":
        st.error("Se requiere un numero telefónico válido y no vacio")
    else:
        if st.button(label = "Registrar cliente", key = "confirm_client_data", help = "Subir los datos al sistema", disabled = add_client_name == "" or not validar_entrada(add_client_name) or add_client_lastname == "" or not validar_entrada(add_client_lastname) or add_client_cellphone == ""):
            add_new_client(add_client_name, add_client_lastname, add_client_colony, add_client_address, add_client_cellphone)

        
def mod_client(id, name, lastname, colony, address, cellphone):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="fitnes_style_db"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()
    if colony == None and address == None:
        #st.error("1")
        cursor.execute(f"UPDATE client SET name = '{name}', lastname = '{lastname}', colony = NULL, address = NULL, cellphone = '{cellphone}' where id = {id}")
    elif address == None and not colony == None:
        #st.error("2")
        cursor.execute(f"UPDATE client SET name = '{name}', lastname = '{lastname}', colony = '{colony}', address = NULL, cellphone = '{cellphone}' where id = {id}")
    elif colony == None and not address == None:
        #st.error("3")
        cursor.execute(f"UPDATE client SET name = '{name}', lastname = '{lastname}', colony = NULL, address = '{address}', cellphone = '{cellphone}' where id = {id}")
    else:
        cursor.execute(f"UPDATE client SET name = '{name}', lastname = '{lastname}', colony = '{colony}', address = '{address}', cellphone = '{cellphone}' where id = {id}")
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def query_clients():
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
        cursor.execute("SELECT * FROM client")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()






def consulta_deuda_clientes(with_debt):
    try:

        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        cursor = conn.cursor()
        if with_debt:
            cursor.execute("SELECT id, concat(name, ' ', lastname), debt, debt_comment  FROM client where debt >= 1")
        else:
            cursor.execute("SELECT id, concat(name, ' ', lastname), cellphone, debt, debt_comment  FROM client")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()


def pay_back_debt(id, ammount, comment):
    try:

        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        cursor = conn.cursor()
        cursor.execute(f"UPDATE client SET debt = debt - {ammount}, debt_comment = '{comment}' WHERE id = {id}")
        progress_text = "Realizando pago ..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        conn.commit()
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()


resultados = consulta_deuda_clientes(False)

df = pd.DataFrame(resultados, columns = ["id","Nombre completo","Telefono celular","Balance (Deuda)","Comentarios"])

st.subheader('Balance de deudas de clientes',)
st.write("Un balance negativo se refiere a deuda del comercio al cliente")
if len(df) > 5:
    st.dataframe(df, hide_index=1, height = 248)
else:
    st.dataframe(df, hide_index=1)
#st.button(label = "Recargar")


st.subheader(body = "Pago de deudas")
query_debt_clients = consulta_deuda_clientes(True)
if not query_debt_clients:
    st.info(body = "No hay clientes con una deuda actual!", icon = "✔")
else:
    id_client = [fila[0] for fila in query_debt_clients]
    name_client = [fila[1] for fila in query_debt_clients]
    debt_client = [fila[2] for fila in query_debt_clients]
    debt_comment_client = [fila[3] for fila in query_debt_clients]
    name_client_to_pay = st.selectbox(label = "Cliente que pagará deuda", options = name_client)
    index_client_to_pay = name_client.index(name_client_to_pay)
    payment_col1, payment_col2 = st.columns(2)
    with payment_col1:
        ammount_to_pay = st.number_input(label = "Monto a pagar", min_value = 0, max_value = debt_client[index_client_to_pay], value = 0, step = 100)
    with payment_col2:
        st.info(body = f"La deuda total es de ${debt_client[index_client_to_pay]}")
    comment_client_to_pay = st.text_area(label = "Comentarios", value = debt_comment_client[index_client_to_pay])
    if ammount_to_pay == 0:
        st.info(body = "Agrega una cantidad a pagar")
    else:
        if st.button(label = f"Pagar ${ammount_to_pay}"):
            pay_back_debt(id_client[index_client_to_pay], ammount_to_pay, comment_client_to_pay)

# Obtener los resultados de la consulta
resultados = query_clients()
id_client = [fila[0] for fila in resultados]
name_client = [fila[1] for fila in resultados]
lastname_client = [fila[2] for fila in resultados]
colony_client = [fila[3] for fila in resultados]
address_client = [fila[4] for fila in resultados]
cellphone_client = [fila[5] for fila in resultados]
debt_client = [fila[6] for fila in resultados]
comment_client = [fila[7] for fila in resultados]
# Combinar nombres y apellidos en una lista
full_name_client = [f"{nombre} {apellido}" for nombre, apellido in zip(name_client, lastname_client)]





st.subheader(body = "Modificar cliente existente")
try:
    mod_name_client = st.selectbox("Cliente", full_name_client, key="mod_name_client")
    mod_name = st.checkbox(label = "Modificar nombre", value = False, key = "mod_name?", help = "Modificar también el nombre del cliente seleccionado")
    mod_index_client = full_name_client.index(mod_name_client)
    mod_id = id_client[mod_index_client]
        
    if mod_name:
        col1_mod_name, col2_mod_lastname = st.columns(2)
        with col1_mod_name:
            mod_new_name_client = st.text_input(label = "Nuevo nombre", max_chars = 255, placeholder = "Juan", value = name_client[mod_index_client], key = "mod_new_name_client")
        with col2_mod_lastname:
            mod_new_lastname_client = st.text_input(label = "Nuevo apellido", max_chars = 255, placeholder = "Ramirez", value = lastname_client[mod_index_client], key = "mod_new_lastname_client")

    else:
        mod_new_name_client = name_client[mod_index_client]
        mod_new_lastname_client = lastname_client[mod_index_client]

    col1_mod_product, col2_mod_product, col3_mod_product = st.columns([3, 5, 2])

    with col1_mod_product:
        colony_value = colony_client[mod_index_client]
        if colony_value is None:
            colony_value = ""  # Si es None, asigna una cadena vacía
        mod_colony_client = st.text_input(label="Colonia", value=colony_value, key="mod_colony_client")
        if mod_colony_client == "":
            mod_colony_client = None  # Si es None, asigna una cadena vacía

    
    with col2_mod_product:
        address_value = address_client[mod_index_client]
        if address_value is None:
            address_value = ""  # Si es None, asigna una cadena vacía
        mod_address_client = st.text_input(label = "Dirección", value = address_value, key = "mod_address_client")
        if mod_address_client == "":
            mod_address_client = None  # Si es None, asigna una cadena vacía

    with col3_mod_product:
        mod_cellphone_client = st.text_input(label = "Telefono de contacto", value = cellphone_client[mod_index_client], key = "mod_cellphone_client")

    
    st.info(body = "El cliente cambiarará en lo siguiente", icon = "✔")

    # Datos individuales
    old_data = {
        '': ['Antes del cambio', 'Después del cambio'],
        'Nombre': [name_client[mod_index_client], mod_new_name_client],
        'Apellido': [lastname_client[mod_index_client], mod_new_lastname_client],
        'Colonia': [colony_client[mod_index_client], mod_colony_client],
        'Dirección': [address_client[mod_index_client], mod_address_client],
        'Telefono de contacto': [cellphone_client[mod_index_client], mod_cellphone_client]
    }

    df = pd.DataFrame(old_data)
    st.dataframe(data = df, hide_index = True)
    if st.button(label = "Modificar cliente", disabled = mod_new_name_client == "" or not validar_entrada(mod_new_name_client) or mod_new_lastname_client == "" or not validar_entrada(mod_new_lastname_client), key = "confirm_mod_client"):
        mod_client(mod_id, mod_new_name_client, mod_new_lastname_client, mod_colony_client, mod_address_client, mod_cellphone_client)
except ValueError:
    st.warning("No hay clientes registrados")
