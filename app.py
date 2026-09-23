import streamlit as st
import requests

def buscar_clientes_gratis(tipo_negocio, localidad):
    url = "https://nominatim.openstreetmap.org/search"
    
    # Nominatim requiere identificar quién hace la consulta
    headers = {
        'User-Agent': 'AppVentasUsuario/1.0'
    }
    
    # Estructuramos la búsqueda
    params = {
        'q': f"{tipo_negocio} en {localidad}",
        'format': 'json',
        'addressdetails': 1,
        'limit': 30 # Máximo de resultados por búsqueda
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return []

st.title("Buscador de Clientes Potenciales")

# Instrucciones ajustadas para OpenStreetMap
tipo_negocio = st.text_input("¿Qué tipo de negocio buscas? (ej. ferretería, farmacia, fábrica)")
localidad = st.text_input("¿En qué ciudad o sector? (ej. Concepción)")

if st.button("Buscar Prospectos"):
    if tipo_negocio and localidad:
        with st.spinner("Buscando en bases de datos públicas..."):
            resultados = buscar_clientes_gratis(tipo_negocio, localidad)
            
            # Filtramos para mostrar solo resultados que tengan un nombre comercial
            negocios_validos = [lugar for lugar in resultados if "name" in lugar and lugar["name"]]
            
            if negocios_validos:
                st.success(f"Se encontraron {len(negocios_validos)} posibles clientes.")
                for lugar in negocios_validos:
                    st.subheader(lugar.get("name"))
                    st.write(f"📍 Dirección: {lugar.get('display_name')}")
                    st.write("---")
            else:
                st.warning("No se encontraron negocios. Intenta usar palabras más generales como 'taller', 'mercado' o 'clínica'.")
    else:
        st.error("Por favor, ingresa el tipo de negocio y la localidad.")
