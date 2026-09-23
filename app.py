import streamlit as st
import requests

# Configuración de la API de Google (requiere tu propia clave)
API_KEY = "TU_API_KEY_AQUI"

def buscar_clientes(producto, localidad):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    # Se estructura la búsqueda para encontrar negocios relacionados al producto
    query = f"empresas o negocios relacionados con {producto} en {localidad}"
    
    params = {
        "query": query,
        "key": API_KEY,
        "language": "es"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

st.title("Buscador de Clientes Potenciales")

producto = st.text_input("¿Qué producto deseas vender?")
localidad = st.text_input("¿En qué ciudad o sector?")

if st.button("Buscar Prospectos"):
    if producto and localidad:
        with st.spinner("Buscando..."):
            resultados = buscar_clientes(producto, localidad)
            
            if resultados:
                st.success(f"Se encontraron {len(resultados)} posibles clientes.")
                for lugar in resultados:
                    st.subheader(lugar.get("name"))
                    st.write(f"📍 Dirección: {lugar.get('formatted_address')}")
                    # Nota: Para extraer números de teléfono se usa la API 'Place Details'
                    st.write("---")
            else:
                st.warning("No se encontraron negocios con esos criterios.")
    else:
        st.error("Por favor, ingresa el producto y la localidad.")