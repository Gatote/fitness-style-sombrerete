import pandas as pd
import mysql.connector
import streamlit as st
import time
st.title("Ventas")

def query_sales(query):
    try:
        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

def consulta_productos():
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
        cursor.execute("SELECT * FROM product")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()
        
def query_client():
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
        cursor.execute("SELECT id,name FROM client")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()
resultados = query_client()
id_client = [fila[0] for fila in resultados]
name_client = [fila[1] for fila in resultados]

def current_date():
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
        cursor.execute("SELECT CURRENT_DATE")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

def new_sale(id_client):
    try:
        date = current_date()[0][0]
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
        cursor.execute(f"INSERT INTO sale (date, id_client) VALUES ('{date}', {id_client})")
        conn.commit()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()
        
def new_sale_product(id_sale, id_product, quantity):
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
        cursor.execute(f"INSERT INTO sale_product (id_sale, id_product, quantity) VALUES ({id_sale}, {id_product}, {quantity})")
        conn.commit()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

def check_sale_id():
    try:
        date = current_date()[0][0]
        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        # Crear un cursor para ejecutar comandos en la base de datos
        cursor = conn.cursor()
        # Ejecutar una consulta SQL real para seleccionar el máximo ID de venta
        cursor.execute("SELECT MAX(id) FROM sale")
        resultado = cursor.fetchone()  # Obtener el resultado
        if resultado:
            max_id = int(resultado[0])  # Convertir el resultado a entero
            return max_id
        else:
            return None  # Retornar None si no se encontraron registros
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

        
# Obtener los resultados de la consulta
resultados = consulta_productos()
id_product = [fila[0] for fila in resultados]
name_client = [fila[1] for fila in resultados]
description_product = [fila[2] for fila in resultados]
quantity_product = [fila[3] for fila in resultados]
price_product = [fila[4] for fila in resultados]
cost_product = [fila[5] for fila in resultados]
profit_product = [fila[6] for fila in resultados]

st.header(body = "Agregar venta")
selected_client = st.selectbox(label = "Seleccione el cliente", options = name_client, key = "list_clients")
id_client = id_client[name_client.index(selected_client)]
if selected_client:
    selected_products = st.multiselect(label = "Seleccione los productos", options = name_client, key = "list_products")

    total = 0
    quantity_products = list()
    for i in selected_products:
        col1_quantity, col2_quantity = st.columns(2)
        product_index = name_client.index(i)
        with col1_quantity:
            quantity_selected_product = st.slider(label = f"Cantidad de {i} {description_product[product_index]}", min_value = 1, max_value = quantity_product[product_index], key = f"{i}_quantity")
            quantity_products.append(quantity_selected_product)
        with col2_quantity:
            if quantity_selected_product != 1:
                ss = "unidades"
            else:
                ss = "unidad"
            st.info(body = f"precio: {price_product[product_index]} * {quantity_selected_product} {ss} ${price_product[product_index]*quantity_selected_product}")
            total = total + price_product[product_index] * quantity_selected_product

    #st.write(quantity_products)
    if selected_products != []:
        if total != 0:
            st.success(body = f"El total de la cuenta será de: ${total}")
            if st.button(label = "Confirmar", key = "add_new_sale", help = "Completar venta de los productos seleccionado anteriormente", ):
                cont = 0
                new_sale(id_client)
                id_sale_new_sale_product = check_sale_id()
                for i in selected_products:
                    id_product_new_sale_product = id_product[name_client.index(i)]
                    quantity_new_sale_product = quantity_products[cont]
                    st.write("")
                    new_sale_product(id_sale_new_sale_product, id_product_new_sale_product, quantity_new_sale_product)
                    cont = cont + 1





st.header(body ='Listado de ventas')
censorship_level = st.selectbox(label = "Seleccione como visualizar las ventas", options = ["Ventas con fecha y clientes", "Ventas con productos, clientes y total", "Ventas con productos, clientes, costos y ganancias"])

if censorship_level == "Ventas con fecha y clientes":
    query = "SELECT s.id,s.date, c.name FROM sale s INNER JOIN client c"
    query_columns = ["Id", "Fecha", "Nombre"]
elif censorship_level == "Ventas con productos, clientes y total":
    query = "SELECT sp.id_sale, CONCAT(c.name, ' ',c.lastname), p.name, p.price * sp.quantity FROM sale_product sp INNER JOIN product p ON p.id = sp.id_product INNER JOIN sale s on s.id = sp.id_sale INNER JOIN client c ON c.id = s.id_client "
    query_columns = ["Id", "Cliente", "Producto", "total"]
elif censorship_level == "Ventas con productos, clientes, costos y ganancias":
    query = "SELECT *  FROM sales_info"
    query_columns = ["Id", "Fecha", "Productos (cantidades)", "Costo total", "Precio total", "Ganancia total", "Nombre del cliente"]
else:
    query = "SELECT 'Hubo un error interno'"

resultados = query_sales(query)

df = pd.DataFrame(resultados, columns = query_columns)

st.write("Agrupado de ventas, los precios individuales se muestran en el concentrado de produtos")
st.dataframe(df, hide_index=1)