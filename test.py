
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st. set_page_config(layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("<h1 style='text-align: center;'>CUMA</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>METAL MANUFACTURING SA DE CV</h4>", unsafe_allow_html=True)

# Limpiar variables de forma RFQ 


# Inicializar variables, cliente_input, user_name

if 'client_input' not in st.session_state or 'user_name' not in st.session_state or 'descripcion' not in st.session_state or 'pm_asignado' not in st.session_state or 'rfq_inquiry_date' not in st.session_state or 'rfq_mail' not in st.session_state or 'numero_RFQ' not in st.session_state:
    st.session_state.client_input = ''
    st.session_state.user_name = ''
    st.session_state.descripcion = ''
    st.session_state.pm_asignado = ''
    st.session_state.rfq_inquiry_date = ''
    st.session_state.rfq_mail = ''
    st.session_state.numero_RFQ = ''  # Inicializar numero_RFQ aquí



# Mostrar dataframes RFQ_Control & Clientes_df

col_izq, col_der = st.columns([3, 1])

col_izq.subheader("RFQ control")
rfq_control = conn.read(worksheet="1 rfq control",ttl=5)
rfq_control = rfq_control.dropna(how = 'all')
col_izq.write(rfq_control.tail(5))

col_der.subheader("Control clientes")
clientes_df = conn.read(worksheet="clientes_df", ttl=5)
clientes_df = clientes_df.dropna(how = 'all')
col_der.write(clientes_df)

# Función para actualizar el DataFrame y obtener el número de RFQ

def actualizar_consecutivo(cliente):
    print("Cliente ingresado:", cliente)
    print("Valores en la columna 'cliente':", clientes_df['cliente'].values)
    
    # Verificar si el cliente existe en el DataFrame
    if cliente in clientes_df['cliente'].values:
        st.write("Cliente encontrado en la base de datos.")
        # Obtener el índice del cliente en el DataFrame
        idx = clientes_df.index[clientes_df['cliente'] == cliente].tolist()[0]
        st.write("Índice del cliente encontrado:", idx)
        # Incrementar la columna 'consecutivo_de_cliente' en 1
        clientes_df.at[idx, 'consecutivo_de_cliente'] += 1
        clientes_df['consecutivo_de_cliente'] = clientes_df['consecutivo_de_cliente'].astype(int)
        # Actualizar la columna 'orden_RFQ' del registro correspondiente
        clientes_df.at[idx, 'orden_RFQ'] = f"{clientes_df.at[idx, 'id_cliente']}-{clientes_df.at[idx, 'consecutivo_de_cliente']}"
        # Guardar el valor actualizado de 'orden_RFQ' en la variable 'numero_RFQ'
        st.session_state.numero_RFQ = clientes_df.at[idx, 'orden_RFQ']
        st.success(f"Se ha actualizado el consecutivo para el cliente {cliente}. Número de RFQ: {st.session_state.numero_RFQ}")
        conn.update(worksheet="clientes_df", data= clientes_df)
    else:
        print("Cliente no encontrado en la base de datos.")
        st.error(f"No se encontró el cliente {cliente} en la base de datos.")

# Función para mostrar orden_RFQ actual

def show_current_ordenRFQ(customer):
    # Verificar si el cliente existe en el DataFrame
    if customer in clientes_df['cliente'].values:
        # Obtener el índice del cliente
        idx = clientes_df.index[clientes_df['cliente'] == customer].tolist()[0]
        # Obtener el valor de 'orden_RFQ' correspondiente
        orden_RFQ = clientes_df.at[idx, 'orden_RFQ']
        return orden_RFQ
    else:
        return None



# Entrada de dato para cliente_input
def customer():
    st.session_state.client_input = st.session_state.customer_key
    st.session_state.customer_key = None

client_input = st.selectbox('Cliente', ('ETM', 'WOLVENG', 'BOSCH','BRP','UL','CONTROL DIGITAL','3CON','BAKER HUGHES','PLASTICSMART',
                                         'SAARGUMMI','EPS','NRMACHINING','CRG','KIMBERLY CLARK','DIICSA','DACOM','HARMAN','XOMERTRY',
                                         'ICARUS','THYSSENKRUPP','SHUNK','IBERFLUID'), index=None, placeholder="Selecciona cliente", key='customer_key', on_change=customer)

st.write(f'Cliente seleccionado: {st.session_state.client_input}')

# Mostrar ultimo numero de orden_RFQ

if st.button("Mostrar Orden RFQ"):
    orden_RFQ = show_current_ordenRFQ(st.session_state.client_input)
    if orden_RFQ is not None:
        st.success(f"El valor actual de orden RFQ para {st.session_state.client_input} es: {orden_RFQ}")
    else:
        st.error(f"No se encontró el cliente {st.session_state.client_input} en la base de datos.")

st.divider()

# Entrada de dato para user_name

def username():
    st.session_state.user_name = st.session_state.user_name_key
    st.session_state.user_name_key = ''

st.text_input('Nombre y apellido de usuario', key='user_name_key', on_change=username, placeholder="Proporciona nombre + apellido")

st.write(f'Nombre de usuario proporcionado: {st.session_state.user_name}')
st.divider()
    
# Entrada de dato para descripcion

def description():
    st.session_state.descripcion = st.session_state.descripcion_key
    st.session_state.descripcion_key = ''

st.text_input('Descripción', key='descripcion_key', on_change=description, placeholder='Describe la pieza a fabricar')

st.write(f'Descripción proporcionada: {st.session_state.descripcion}')
st.divider()

# Entrada de dato para pm_asignado
def assigned_pm():
    st.session_state.pm_asignado = st.session_state.pm_asignado_key
    st.session_state.pm_asignado_key = None

pm_asignado = st.selectbox('Project Manager asignado', ('Rodrigo Ramirez', 'Elian Sanabria','Sergio Santos'), index=None, placeholder="Selecciona encargado", key='pm_asignado_key', on_change=assigned_pm)
st.write(f'Representante de CUMA para el proyecto: {st.session_state.pm_asignado}')
st.divider()

# Entrada de dato para rfq_inquiry_date
def inquiry_date():
    st.session_state.rfq_inquiry_date = st.session_state.rfq_inquiry_date_key
    st.session_state.rfq_inquiry_date_key = None

rfq_inquiry_date = st.date_input("Fecha en que se solicita RFQ", format="DD.MM.YYYY", value=None, key='rfq_inquiry_date_key', on_change=inquiry_date)

st.write(f'Fecha en que se solicita la cotización {st.session_state.rfq_inquiry_date}')
st.divider()

# Entrada de dato para RFQ_email

def email_keywords():
    st.session_state.rfq_mail = st.session_state.rfq_mail_key
    st.session_state.rfq_mail_key = ''

rfq_mail = st.text_input("Palabras clave de correo", placeholder="Texto para buscar en correo", key='rfq_mail_key', on_change=email_keywords)

st.write(f'Texto clave a buscar en el correo: {st.session_state.rfq_mail}')
st.divider()

# Creación de status como primer status = open

st.session_state.order_status = "Open"

st.write("El status de la orden comienza en: ", st.session_state.order_status)

# Boton para crear RFQ

if st.button("Crear RFQ"):
     actualizar_consecutivo(st.session_state.client_input)
     st.success(f"Nuevo número de RFQ para el cliente {st.session_state.client_input}: {st.session_state.numero_RFQ}")

# Mostrar los datos a cargar

st.markdown("<h4 style='text-align: center;'>Datos a cargar </h4>", unsafe_allow_html=True)

new_data = {
    "RFQ_num": [st.session_state.numero_RFQ],
    "RFQ_mail": [st.session_state.rfq_mail],
    "RFQ_inquiry_date": [st.session_state.rfq_inquiry_date],
    "PM_asignado": [st.session_state.pm_asignado],
    "Cliente": [st.session_state.client_input],
    "Usuario":[st.session_state.user_name],
    "Descripcion": [st.session_state.descripcion],
    "Status": [st.session_state.order_status]
}   

my_df = pd.DataFrame(new_data)

st.write(my_df)
st.warning("Revisar si los datos están correctos para poder cargarlos al sistema y confirmar")


#Agregar datos a la base principal RFQ Control

borrar_datos = st.button("Agregar datos" )


# Restablecer valores cuando se agregan datos a df
    
if borrar_datos:
    rfq_control = rfq_control.append(my_df, ignore_index=True)
    st.header("New File")
    st.write(rfq_control.tail(5))
    conn.update(worksheet="1 rfq control", data= rfq_control)

    
    





