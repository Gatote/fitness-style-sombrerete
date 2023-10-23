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
        return resultados[0][0]
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

def min_date():
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
        cursor.execute("SELECT min(date) FROM sale")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        return resultados[0][0]
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()


def new_sale(id_client, date):
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

def check_sale_id():
    try:
        date = current_date()
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

       
def update_client_debt(id_client, total_debt, comment):
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
        cursor.execute(f"UPDATE client SET debt = debt + {total_debt}, debt_comment = '{comment}' WHERE id = {id_client}")
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

st.header(body = "Agregar venta")
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
        change_date_col1, change_date_col2 = st.columns(2)
        with change_date_col1:
            change_date_for_sale = st.checkbox(label = "Escojer fecha específica para la venta", value = False, key = "change_date_for_sale", help = "Cambiar fecha que se registrará en la venta, por defecto se introduce la fecha actual")
            if change_date_for_sale:
                with change_date_col2:
                    new_date_for_sale = st.date_input(label = "Fecha deseada", value = current_date(), min_value = None, max_value = None, key = "date_for_sale", help = "Fecha que se registrará en la venta")
        selected_products = st.multiselect(label = "Seleccione los productos", options = name_product, key = "list_products")
        total = 0
        quantity_products = list()
        new_price_products = list()
        new_cost_products = list()
        for i in selected_products:
            col1_quantity, col2_quantity, col3_quantity = st.columns([2, 4.5, 4.5])
            product_index = name_product.index(i)
            with col1_quantity:
                edit_price = st.checkbox(label = "Modificar precio", value = False, key = f"{i}_edit_price", help = f"Modificar el precio de venta de {i}")

            with col2_quantity:
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
            with col3_quantity:
                if quantity_selected_product != 1:
                    ss = "unidades"
                else:
                    ss = "unidad"
                if not edit_price:
                    st.info(body = f"precio: {price_product[product_index]} * {quantity_selected_product} {ss} ${price_product[product_index]*quantity_selected_product}")
                    total = total + price_product[product_index] * quantity_selected_product
                    mod_price_product = price_product[product_index]
                    new_price_products.append(mod_price_product)
                    new_cost_products.append(cost_product[product_index])
                else:
                    col1_price_product, col2_price_product = st.columns(2)
                    with col1_price_product:
                        mod_price_product = st.number_input(label = f"Precio de {i  }", min_value = 0, max_value = 99999, value = int(price_product[product_index]), step = 1, key = f"{i}_price_product")
                    with col2_price_product:
                        st.info(body = f"{quantity_selected_product} {ss} ${mod_price_product*quantity_selected_product}")
                        total = total + mod_price_product * quantity_selected_product
                    new_price_products.append(mod_price_product)
                    new_cost_products.append(cost_product[product_index])

        #st.write(quantity_products)
        if selected_products != []:
            if total != 0:
                st.success(body = f"El total de la cuenta será de: ${total}")
                total_payment = st.number_input(label = "Total de pago", min_value = 0, max_value = int(total), value = int(total))
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

                        if change_date_for_sale:
                            date = new_date_for_sale
                        else:
                            date = current_date()

                        new_sale(id_client, date)
                        id_sale_new_sale_product = check_sale_id()
                        for i in selected_products:
                            id_product_new_sale_product = id_product[name_product.index(i)]
                            quantity_new_sale_product = quantity_products[cont]
                            final_price_product = new_price_products[cont]
                            final_cost_product = new_cost_products[cont]
                            st.write("")
                            new_sale_product(id_sale_new_sale_product, id_product_new_sale_product, quantity_new_sale_product, final_price_product, final_cost_product)
                            cont = cont + 1
                        if sale_with_debt:
                            update_client_debt(id_client, debt, debt_comments)
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




resultados = query_sales("SELECT count(id) FROM sale")

if resultados and resultados[0][0] > 0:
    st.header(body='Listado de ventas')
    censorship_level = st.selectbox(label="Seleccione cómo visualizar las ventas", options=["Ventas con fecha y clientes", "Ventas con productos, clientes y total", "Ventas con productos, clientes, costos y ganancias"])


    min_date_for_query = min_date()
    max_date_for_query = current_date()
    if st.checkbox(label = "Ajustar rángo de fechas", value = False, key = "date_range", help = "Elegir una fecha de inicio y una fecha final para ver un rango de ventas"):
        min_date_for_query = st.date_input(label = "Fecha desde", value = min_date(), min_value = min_date(), max_value = current_date(), key = "since_date", help = "Fecha desde comenzará a mostrar las ventas")
        max_date_for_query = st.date_input(label = "Fecha hasta", value = current_date(), min_value = min_date(), max_value = current_date(), key = "to_date", help = "Fecha desde comenzará a mostrar las ventas")

    if censorship_level == "Ventas con fecha y clientes":
        query = f"SELECT s.id, s.date, c.name FROM sale s INNER JOIN client c WHERE s.date >= '{min_date_for_query}' and s.date <= '{max_date_for_query}' ORDER BY id DESC"
        query_columns = ["Id", "Fecha", "Nombre"]
    elif censorship_level == "Ventas con productos, clientes y total":
        query = f"SELECT sp.id_sale, CONCAT(c.name, ' ', c.lastname), p.name, p.price * sp.quantity FROM sale_product sp INNER JOIN product p ON p.id = sp.id_product INNER JOIN sale s on s.id = sp.id_sale INNER JOIN client c ON c.id = s.id_client WHERE s.date >= '{min_date_for_query}' and s.date <= '{max_date_for_query}' ORDER BY s.id DESC"
        query_columns = ["Id", "Cliente", "Producto", "Total"]
    elif censorship_level == "Ventas con productos, clientes, costos y ganancias":
        query = f"SELECT *  FROM sales_info WHERE sale_date >= '{min_date_for_query}' and sale_date <= '{max_date_for_query}' ORDER BY sale_number DESC"
        query_columns = ["Id", "Fecha", "Productos (cantidades)", "Costo total", "Precio total", "Ganancia total", "Nombre del cliente"]
    else:
        query = "SELECT 'Hubo un error interno'"




    #st.write(query)
    resultados = query_sales(query)

    if resultados and censorship_level == "Ventas con productos, clientes, costos y ganancias":
        # Convert Decimal objects to floats and create a new list of lists
        modified_resultados = []
        for row in resultados:
            modified_row = list(row)
            modified_row[5] = float(modified_row[5])  # Assuming that the "Ganancia total" column is at index 5
            modified_resultados.append(modified_row)

        df = pd.DataFrame(modified_resultados, columns=query_columns)

        st.write("Agrupado de ventas, los precios individuales se muestran en el concentrado de productos")
        
        if len(df) > 5:
            st.dataframe(df, hide_index=1, height = 248)
        else:
            st.dataframe(df, hide_index=1)
    elif resultados:

        df = pd.DataFrame(resultados, columns=query_columns)

        st.write("Agrupado de ventas, los precios individuales se muestran en el concentrado de productos")
        
        if len(df) > 5:
            st.dataframe(df, hide_index=1, height = 248)
        else:
            st.dataframe(df, hide_index=1)

else:
    st.warning(body = "No hay ventas registradas", icon = "⚠")





def update_sale_product(id_sale, id_product, quantity, final_price, final_cost):
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
        cursor.execute(f"UPDATE sale_product SET quantity = {quantity}, final_price = {final_price}, final_cost = {final_cost} WHERE id_sale = {id_sale} AND id_product = {id_product}")
        #st.write(f"INSERT INTO sale_product (id_sale, id_product, quantity, final_price, final_cost, final_profit) VALUES ({id_sale}, {id_product}, {quantity}, {final_price}, {final_cost}, {final_price} - {final_cost})")
        conn.commit()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()



def query_sales_mod():
    try:
        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM sale")  # Selecciona solo los IDs de las ventas
        resultados = cursor.fetchall()
        return [row[0] for row in resultados]  # Devuelve una lista de IDs
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

def delete_sale(id):
    try:
        # Establecer una conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="fitnes_style_db"
        )
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM sale WHERE id = {id}")
        cursor.execute(f"DELETE FROM sale_product WHERE id_sale = {id}")
        conn.commit()
        progress_text = "Eliminando venta ..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()


st.subheader("Modificar venta")
# Obtiene la lista de IDs de ventas
ids_ventas = query_sales_mod()

if not ids_ventas:
    st.info(body = "No hay ventas Registradas")
else:
    # Crea un select box para seleccionar el número de venta
    numero_venta = st.selectbox("Número de Venta", ids_ventas)
    if st.checkbox(label = "Cancelar venta", value = False, key = "cancel_sale"):
        if st.button(label = "Confirmar", key = "confirm_cancel_sale"):
            delete_sale(numero_venta)
    else:
        # Luego, puedes usar el número de venta seleccionado para realizar otras consultas o acciones según tus necesidades.
        # Por ejemplo, puedes mostrar los detalles de la venta seleccionada en otro lugar de la aplicación.

        # Para obtener los detalles de la venta seleccionada:
        def obtener_detalle_venta(numero_venta):
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="admin",
                    password="admin",
                    database="fitnes_style_db"
                )
                cursor = conn.cursor()
                cursor.execute(f"SELECT id_sale, id_product, p.name, sp.quantity, st.total_pieces_in_stock + sp.quantity, final_price, final_cost, final_profit FROM sale_product sp INNER JOIN product p on p.id = sp.id_product INNER JOIN stock st on st.product_id = p.id WHERE sp.id_sale = {numero_venta}")
                #st.write(f"SELECT id_sale, id_product, p.name, sp.quantity, st.total_pieces_in_stock + sp.quantity, final_price, final_cost, final_profit FROM sale_product sp INNER JOIN product p on p.id = sp.id_product INNER JOIN stock st on st.product_id = p.id WHERE sp.id_sale = {numero_venta}")
                resultados = cursor.fetchall()  # Obtener todas las filas correspondientes a la venta
                return resultados
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                conn.close()

        detalles_venta = obtener_detalle_venta(numero_venta)
        id_sale = [fila[0] for fila in detalles_venta]
        id_product = [fila[1] for fila in detalles_venta]
        name_productt = [fila[2] for fila in detalles_venta]
        quantity_product = [fila[3] for fila in detalles_venta]
        quantity_product_avalaible = [fila[4] for fila in detalles_venta]
        price_product = [fila[5] for fila in detalles_venta]
        cost_product = [fila[6] for fila in detalles_venta]
        profit_product = [fila[7] for fila in detalles_venta]

        # if numero_venta is not None:
        #     if detalles_venta:
        #         st.subheader("Detalles de la Venta Seleccionada")
        #         df_detalle_venta = pd.DataFrame(detalles_venta, columns=["id_sale", "id_product", "p.name", "sp.quantity", "Cantidad disponible", "final_price", "final_cost", "final profit"])
        #         st.dataframe(df_detalle_venta, hide_index=True)
            
        #name_product
        # Convierte ambas listas en conjuntos
        set_a = set(name_product)
        set_b = set(name_productt)

        # Crea una nueva lista con los elementos de b que no están en a
        ramaining_products = [x for x in name_productt if x not in name_product]

        selected_products = st.multiselect(label = "Seleccione los productos a modificar de la venta", options = name_productt, key = "list_of_products_from_sale_to_modify")
        if ramaining_products:
            selected_products_to_add = st.multiselect(label = "Seleccione los productos a agregar en la venta", options = ramaining_products, key = "list_of_products_to_add_to_sale")

        total = 0
        quantity_products = list()
        new_price_products = list()
        new_cost_products = list()
        for i in selected_products:
            col1_quantity, col2_quantity, col3_quantity = st.columns([2.2, 4.3, 4.5])
            product_index = name_productt.index(i)
            with col1_quantity:
                edit_price = st.checkbox(label = "Modificar precio", value = False, key = f"{i}_edit_price_in_sale", help = f"Modificar el precio de venta de {i}")

            with col2_quantity:
                quantity = int(quantity_product[product_index])
                if quantity_product_avalaible[product_index] > 0:
                    quantity_selected_product = st.slider(label = f"Cantidad de {i}", min_value = 0, max_value = int(quantity_product_avalaible[product_index]), value = quantity_product[product_index], key = f"{i}_quantity_to_modify")
                else:
                    quantity_selected_product = 0
                    st.warning(f"No hay {i} en existencia!")

                quantity_products.append(quantity_selected_product)
            with col3_quantity:
                if quantity_selected_product != 1:
                    ss = "unidades"
                else:
                    ss = "unidad"
                if not edit_price:
                    st.info(body = f"precio: {price_product[product_index]} * {quantity_selected_product} {ss} ${price_product[product_index]*quantity_selected_product}")
                    total = total + price_product[product_index] * quantity_selected_product
                    mod_price_product = price_product[product_index]
                    new_price_products.append(mod_price_product)
                    new_cost_products.append(cost_product[product_index])
                else:
                    col1_price_product, col2_price_product = st.columns(2)
                    with col1_price_product:
                        mod_price_product = st.number_input(label = f"Precio de {i  }", min_value = 0, max_value = 99999, value = int(price_product[product_index]), step = 1, key = f"{i}_price_product_to_modify")
                    with col2_price_product:
                        st.info(body = f"{quantity_selected_product} {ss} ${mod_price_product*quantity_selected_product}")
                        total = total + mod_price_product * quantity_selected_product
                    new_price_products.append(mod_price_product)
                    new_cost_products.append(cost_product[product_index])
        if selected_products != []:
            if total != 0:
                st.success(body = f"El total de la cuenta será de: ${total}")
                total_payment = st.number_input(label = "Total de pago", min_value = 0, max_value = int(total), value = int(total))
                if total_payment != total:
                    if  debt_client > 0:
                        debt_text = f" el cual cuenta con una deuda actual de {debt_client}"
                    else:
                        debt_text = ""
                    st.info(body = f"La diferencia es de ${int(total - total_payment)}, la cual se aumentará a la deuda total del cliente '{selected_client}'{debt_text}", icon = "ℹ")
                    debt = int(total - total_payment)
                    debt_comments = st.text_area(label = "Comentarios", value = f"{debt_comment_client}", key = "comments_client_debt")
                    sale_with_debt = True
                else:
                    sale_with_debt = False
                if st.checkbox(label = "Confirmar datos", value = False, key = "confirm_data_for_edit_sale"):
                    if st.button(label = "Confirmar", key = "edit_sale", help = "Completar venta de los productos seleccionado anteriormente", ):
                        cont = 0
                        id_sale_new_sale_product = numero_venta
                        for i in selected_products:
                            id_product_new_sale_product = id_product[name_product.index(i)]
                            quantity_new_sale_product = quantity_products[cont]
                            final_price_product = new_price_products[cont]
                            final_cost_product = new_cost_products[cont]
                            st.write("")
                            update_sale_product(id_sale_new_sale_product, id_product_new_sale_product, quantity_new_sale_product, final_price_product, final_cost_product)
                            cont = cont + 1
                        if sale_with_debt:
                            update_client_debt(id_client, debt, debt_comments)
                        progress_text = "Realizando venta ..."
                        my_bar = st.progress(0, text=progress_text)
                        for percent_complete in range(100):
                            time.sleep(0.01)
                            my_bar.progress(percent_complete + 1, text=progress_text)
                        time.sleep(1)
                        st.experimental_rerun()