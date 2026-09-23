import streamlit as st
import requests
import json

# Pega aquí la clave que copiaste de Serper.dev
API_KEY = "24f15051826fa884a67cfc2759e383df5137f049"

def buscar_clientes(producto, localidad):
    url = "https://google.serper.dev/places"
    
    # gl="cl" asegura que el algoritmo de búsqueda priorice resultados en Chile
    payload = json.dumps({
      "q": f"{producto} en {localidad}",
      "gl": "cl",
      "hl": "es"
    })
    
    headers = {
      'X-API-KEY': API_KEY,
      'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json().get("places", [])
    
    st.error("Error en la conexión con la base de datos.")
    return []

st.title("Buscador de Clientes Potenciales")
st.caption("Motor de búsqueda: Google Maps (Vía Serper)")

producto = st.text_input("¿Qué producto deseas vender?")
# Dejo Concepción por defecto para acelerar tus pruebas
localidad = st.text_input("¿En qué ciudad o sector?", value="Concepción")

if st.button("Buscar Prospectos"):
    if producto and localidad:
        with st.spinner("Buscando negocios..."):
            resultados = buscar_clientes(producto, localidad)
            
            if resultados:
                st.success(f"Se encontraron {len(resultados)} posibles clientes.")
                for lugar in resultados:
                    st.subheader(lugar.get("title", "Sin nombre comercial"))
                    st.write(f"📍 Dirección: {lugar.get('address', 'Dirección no disponible')}")
                    
                    # Si el negocio tiene un teléfono público, lo mostramos
                    if "phoneNumber" in lugar:
                        st.write(f"📞 Teléfono: {lugar['phoneNumber']}")
                        
                    st.write("---")
            else:
                st.warning("No se encontraron negocios con esos criterios.")
    else:
        st.error("Por favor, ingresa el producto y la localidad.")
