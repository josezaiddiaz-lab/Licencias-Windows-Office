import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Inventario de Licencias", layout="centered")

# --- CONEXIÓN A GOOGLE SHEETS ---
# Asegúrate de tener tu archivo 'credentials.json' en la misma carpeta
def get_sheets_client():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Lista de hojas (pestañas) que identificamos
WORKSHEETS = [
    "CLIENTES VARIOS", "AGENCIA ROJAS", "MARINOIL", "GREMEX", 
    "SUMINISTROS", "SUMYSA", "SYSPSA", "JUAN ALEMAN", "MUNICIPIO", 
    "ALPEN", "MAD", "ARGUELLES", "IOSSIFT", "DELTA", "USPEAK", "CONTROLES FLEXIBLES"
]

# --- INTERFAZ ---
st.title("📦 Inventario de Licencias")

menu = st.selectbox("Selecciona una opción", ["Registrar Licencia", "Ver Inventario"])

if menu == "Registrar Licencia":
    st.subheader("Agregar Nueva Licencia")
    
    # Selección de pestaña
    cliente_tab = st.selectbox("Selecciona la Empresa (Pestaña)", WORKSHEETS)
    
    with st.form("registro_form"):
        # Campos basados en las columnas de tu Excel
        fecha = st.text_input("Fecha de Instalación")
        serie = st.text_input("Serie")
        modelo = st.text_input("Modelo")
        depto = st.text_input("Departamento")
        carac = st.text_input("Características del Equipo")
        usuario = st.text_input("Usuario")
        correo_user = st.text_input("Correo del Usuario")
        clave_user = st.text_input("Clave Usuario")
        win11 = st.text_input("Windows 11 Pro")
        office19 = st.text_input("Office 2019 Pro")
        clave_office_21 = st.text_input("Clave Office Pro Plus 2021")
        clave_office_24 = st.text_input("Clave Office 2024")
        correo_office = st.text_input("Correo de Office")
        pass_office = st.text_input("Contraseña")
        cel_rec = st.text_input("Cel o Correo de Recuperación")
        antivirus = st.text_input("Antivirus")
        obs = st.text_area("Observación")
        
        submit = st.form_submit_button("Guardar Licencia")
        
        if submit:
            try:
                client = get_sheets_client()
                # Ajusta esto al ID de tu hoja de cálculo
                spreadsheet = client.open_by_key("1TxukcYhPDoCKrbqhzbUBKFLauvTRBlwrXq5IH2m0Zs")
                sheet = spreadsheet.worksheet(cliente_tab)
                
                # Datos a insertar
                data = [cliente_tab, fecha, serie, modelo, depto, carac, usuario, 
                        correo_user, clave_user, win11, office19, clave_office_21, 
                        clave_office_24, correo_office, pass_office, cel_rec, antivirus, obs]
                
                sheet.append_row(data)
                st.success(f"Licencia registrada exitosamente en {cliente_tab}")
            except Exception as e:
                st.error(f"Error al guardar: {e}")

elif menu == "Ver Inventario":
    st.subheader("Consultar Inventario")
    cliente_tab = st.selectbox("Selecciona la Empresa para ver", WORKSHEETS)
    
    if st.button("Cargar Datos"):
        try:
            client = get_sheets_client()
            spreadsheet = client.open_by_key("1TxukcYhPDoCKrbqhzbUBKFLauvTRBlwrXq5IH2m0Zs")
            sheet = spreadsheet.worksheet(cliente_tab)
            data = sheet.get_all_records()
            df = pd.DataFrame(data)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error al leer: {e}")