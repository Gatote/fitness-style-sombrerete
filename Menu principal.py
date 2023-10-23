
import pandas as pd
import mysql.connector
import streamlit as st
import time
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
    cursor.execute("SELECT 'si'")
except Exception as e:
    st.info(body = "No hay conexion al servidor")
    exit()
# Configurar la página de Streamlit
st.set_page_config(
    page_title="FITNESS STYLE SOMBRERETE",
    layout="wide",  # Cambiar el diseño a "wide" para aprovechar más espacio horizontal
    initial_sidebar_state="collapsed"  # Colapsar la barra lateral inicialmente
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
        cursor.execute("SELECT id, CONCAT(name, ' ', lastname), debt_comment FROM client")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    except Exception as e:
        st.info(f"No hay conexion al servidor {str(e)}")

st.title(body = "Fitness Style Sombrerete   ")


clients = query_clients()
if clients:
    st.header("Clientes registrados")
    clients_columns=['ID','Nombre', 'Comentarios']
    df_clients = pd.DataFrame(data = clients, columns = clients_columns)

    if len(df_clients) > 5:
        st.dataframe(df_clients, hide_index=1, height = 248)
    else:
        st.dataframe(df_clients, hide_index=1)
    


def consulta_stock():
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
        cursor.execute("SELECT CONCAT(product_id, ' - ', product_name), product_description, total_pieces_in_stock FROM stock ORDER BY total_pieces_in_stock DESC")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()
resultados = consulta_stock()
productos = [fila[0] for fila in resultados]
cantidades = [fila[2] for fila in resultados]
        
# Crear un DataFrame de Pandas con los resultados y establecer los encabezados
df = pd.DataFrame(resultados, columns=['Producto', 'Descripción', 'Cantidad en inventario'])

st.header('Existencia de productos')

# Obtener los resultados de la consulta
col1, col2 = st.columns(2)
with col1:
    producto_seleccionado = st.selectbox("Producto", productos,key="consultar_existencia_producto")
with col2:
    st.write("")
    if producto_seleccionado:
        # Busca el índice del producto seleccionado
        indice = productos.index(producto_seleccionado)
        # Muestra la cantidad correspondiente en el col2
        st.success(f"Hay {cantidades[indice]} unidades de {producto_seleccionado.split(' - ')[1]} en inventario")

if len(df) > 5:
    st.dataframe(df, hide_index=1, height = 248)
else:
    st.dataframe(df, hide_index=1)





# Obtener los resultados de la consulta
resultados = consulta_venta_diaria()
if resultados:

    # Crear un DataFrame de Pandas con los resultados y establecer los encabezados
    df = pd.DataFrame(resultados, columns=['id_venta', 'fecha', 'producto(cantidad)', 'compra', 'venta', 'ganancia', 'nombre_cliente'])

    # Mostrar el DataFrame en Streamlit
    st.subheader('Ventas del día')
    st.dataframe(df, hide_index=1)



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
        cursor.execute("SELECT p.id, p.name, p.description, s.total_pieces_in_stock, p.price, p.cost, p.profit  FROM product p INNER JOIN stock s ON p.id = s.product_id WHERE s.total_pieces_in_stock >= 1")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
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
        cursor.execute("SELECT id, name, debt, debt_comment FROM client")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

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
        
def new_sale_product(id_sale, id_product, quantity, final_price, final_cost):
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
        cursor.execute(f"INSERT INTO sale_product (id_sale, id_product, quantity, final_price, final_cost, final_profit) VALUES ({id_sale}, {id_product}, {quantity}, {final_price}, {final_cost}, {final_price} - {final_cost})")
        #st.write(f"INSERT INTO sale_product (id_sale, id_product, quantity, final_price, final_cost, final_profit) VALUES ({id_sale}, {id_product}, {quantity}, {final_price}, {final_cost}, {final_price} - {final_cost})")
        conn.commit()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

        
resultados = query_client()
id_client = [fila[0] for fila in resultados]
name_client = [fila[1] for fila in resultados]
debt_client = [fila[2] for fila in resultados]
debt_comment_client = [fila[3] for fila in resultados]
# Obtener los resultados de la consulta
resultados = consulta_productos()
id_product = [fila[0] for fila in resultados]
name_product = [fila[1] for fila in resultados]
description_product = [fila[2] for fila in resultados]
quantity_product = [fila[3] for fila in resultados]
price_product = [fila[4] for fila in resultados]
cost_product = [fila[5] for fila in resultados]
profit_product = [fila[6] for fila in resultados]


st.header(body = "Agregar venta rápida")
if name_client:
    selected_client = st.selectbox(label = "Seleccione el cliente", options = name_client, key = "list_clients")
    id_client = id_client[name_client.index(selected_client)]
    debt_client = debt_client[name_client.index(selected_client)]
    debt_comment_client = debt_comment_client[name_client.index(selected_client)]
else:
    st.warning(body = "No hay clientes registrados", icon = "⚠")
    selected_client = None
if selected_client:
    if name_product:
        selected_products = st.multiselect(label = "Seleccione los productos", options = name_product, key = "list_products")
        total = 0
        quantity_products = list()
        new_price_products = list()
        new_cost_products = list()
        for i in selected_products:
            col1_quantity, col2_quantity = st.columns(2)
            product_index = name_product.index(i)

            with col1_quantity:
                quantity = int(quantity_product[product_index])
                if quantity > 1:
                    quantity_selected_product = st.slider(label = f"Cantidad de {i}", min_value = 1, max_value = int(quantity_product[product_index]), key = f"{i}_quantity", help = f"Cantidad a vender de {i} {description_product[product_index]}")
                elif quantity == 1:
                    quantity_selected_product = int(quantity_product[product_index])
                    st.warning(f"Solo hay una unidad de {i} en existencia!")
                else:
                    quantity_selected_product = 0
                    st.warning(f"No hay {i} en existencia!")

                quantity_products.append(quantity_selected_product)
            with col2_quantity:
                if quantity_selected_product != 1:
                    ss = "unidades"
                else:
                    ss = "unidad"
                st.info(body = f"precio: {price_product[product_index]} * {quantity_selected_product} {ss} ${price_product[product_index]*quantity_selected_product}")
                total = total + price_product[product_index] * quantity_selected_product
                mod_price_product = price_product[product_index]
                new_price_products.append(mod_price_product)
                new_cost_products.append(cost_product[product_index])

        #st.write(quantity_products)
        if selected_products != []:
            if total != 0:
                st.success(body = f"El total de la cuenta será de: ${total}")
                total_payment = st.number_input(label = "Total de pago", min_value = 0, max_value = int(total), value = int(total), disabled = True)
                if total_payment != total:
                    if  debt_client > 0:
                        debt_text = f" el cual cuenta con una deuda actual de {debt_client}"
                    else:
                        debt_text = ""
                    st.info(body = f"La diferencia es de ${int(total - total_payment)}, la cual se aumentará a la deuda total del cliente '{selected_client}'{debt_text}", icon = "ℹ")
                    debt = int(total - total_payment)
                    debt_comments = st.text_area(label = "Comentarios", value = f"{debt_comment_client}")
                    sale_with_debt = True
                else:
                    sale_with_debt = False
                if st.checkbox(label = "Confirmar datos", value = False, key = "confirm_data_for_sale"):
                    if st.button(label = "Confirmar", key = "add_new_sale", help = "Completar venta de los productos seleccionado anteriormente", ):
                        cont = 0
                        new_sale(id_client)
                        id_sale_new_sale_product = check_sale_id()
                        for i in selected_products:
                            id_product_new_sale_product = id_product[name_product.index(i)]
                            quantity_new_sale_product = quantity_products[cont]
                            final_price_product = new_price_products[cont]
                            final_cost_product = new_cost_products[cont]
                            st.write("")
                            new_sale_product(id_sale_new_sale_product, id_product_new_sale_product, quantity_new_sale_product, final_price_product, final_cost_product)
                            cont = cont + 1
                        progress_text = "Realizando venta ..."
                        my_bar = st.progress(0, text=progress_text)
                        for percent_complete in range(100):
                            time.sleep(0.01)
                            my_bar.progress(percent_complete + 1, text=progress_text)
                        time.sleep(1)
                        st.experimental_rerun()
    else:
        st.warning(body = "No hay productos en existencia para vender", icon = "⚠")
        st.info(body = "Agrega mas producto desde el apartado de productos", icon = "ℹ")

