import pandas as pd
import mysql.connector
import streamlit as st
import time

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
# Obtener los resultados de la consulta
resultados = consulta_productos()
id_product = [fila[0] for fila in resultados]
name_product = [fila[1] for fila in resultados]
description_product = [fila[2] for fila in resultados]
quantity_product = [fila[3] for fila in resultados]
price_product = [fila[4] for fila in resultados]
cost_product = [fila[5] for fila in resultados]
profit_product = [fila[6] for fila in resultados]

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
        cursor.execute("SELECT * FROM stock")  # Reemplaza 'nombre_de_la_tabla' con el nombre de tu tabla real
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()
# Obtener los resultados de la consulta
resultados = consulta_stock()
productos = [fila[0] for fila in resultados]
cantidades = [fila[2] for fila in resultados]

st.title("Productos",help="Concentrado todo de acerca de los productos, asi mismo las existencias de cada uno")

st.header("Añadir productos")
col1_product, col2_product = st.columns(2)
     
def add_product(id,quantity):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="fitnes_style_db"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT
    cursor.callproc('add_product', (id+1,quantity))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def add_new_product(name_product, description_product, quantity_product, price_product, cost_product, profit_product):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="fitnes_style_db"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT
    cursor.execute(f"INSERT INTO product (name, description, quantity, price, cost, profit) values ('{name_product}', '{description_product}', {quantity_product}, {price_product}, {cost_product}, {profit_product})")
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()


with col1_product:
    st.subheader("Añadir producto existente")
    try:
        añadir_producto_seleccionado = st.selectbox("Producto", name_product, key="añadir_producto_existente")
        indice = name_product.index(añadir_producto_seleccionado)
        id = name_product.index(añadir_producto_seleccionado)
        
        st.text_input("Descripcion",f" {description_product[indice]}",disabled=True)
        cantidad = st.number_input("Cantidad a añadir",value=0,min_value=0,max_value=99999,step=1)


        st.write(f"Se añadirán {cantidad} unidades de {añadir_producto_seleccionado}")
        añadir = st.button("Añadir producto", disabled=cantidad<1 or cantidad>99999)
        if añadir:
            add_product(id,cantidad)
    except ValueError:
        st.warning("No hay productos registrados")

            
with col2_product:
    st.subheader("Añadir producto nuevo")
    add_name_product = st.text_input("Nombre del producto","",255,"añadir_producto_nuevo",placeholder="Producto 1")
    add_descripcion_product = st.text_input("Descripcion del producto","",255,"añadir_descripcion_producto_nuevo",placeholder="Sabor fresa, light")
    add_quantity_product = st.number_input(label = "Cantidad del producto", min_value = 0, max_value = 99999,key = "añadir_cantidad_producto_nuevo", step = 1, value = 0)
    col1_add_new_product, col2_add_new_product, col3_add_new_product = st.columns(3)
    with col1_add_new_product:
        add_price_product = st.number_input(label = "Precio al cliente", min_value = 0, max_value = 99999, value = 0, step = 1, key = "add_price_product")
    with col2_add_new_product:
        add_cost_product = st.number_input(label = "Costo de compra", min_value = 0, max_value = 99999, value = 0, step = 1, key = "add_cost_product")
    with col3_add_new_product:
        add_profit_product = st.number_input(label = "Ganancia", min_value = -99999, max_value = 99999, value = add_price_product - add_cost_product, step = 1, key = "add_profit_product", disabled = True)
    if add_name_product in name_product:
        st.error("El nombre registrado ya existe, usar otro")
    else:
        confirm_add_new_product = st.button("Añadir producto", disabled=add_quantity_product<1 or add_quantity_product>99999 or add_profit_product<0 or add_name_product in name_product,key = "confirm_add_new_product")
        if confirm_add_new_product:
            add_new_product(add_name_product, add_descripcion_product, add_quantity_product, add_price_product, add_cost_product, add_profit_product)




        








# Crear un DataFrame de Pandas con los resultados y establecer los encabezados
df = pd.DataFrame(resultados, columns=['Producto', 'Descripcion', 'Cantidad en inventario'])

# Mostrar el DataFrame en Streamlit
st.subheader('Existencia de productos')
st.dataframe(df, hide_index=1)

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



