import streamlit as st
import requests
import json

# Recuerda pegar tu clave de Serper aquí
API_KEY = "24f15051826fa884a67cfc2759e383df5137f049"

def buscar_clientes(producto, localidad):
    url = "https://google.serper.dev/places"
    
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
localidad = st.text_input("¿En qué sector? (Ej: Centro, Barrio Industrial, Hualpén)")

# Un pequeño consejo en pantalla para tu papá
st.info("💡 Tip: Para obtener más resultados, busca por sectores específicos o barrios en lugar de ciudades completas.")

if st.button("Buscar Prospectos"):
    if producto and localidad:
        with st.spinner("Buscando negocios y fotos..."):
            resultados = buscar_clientes(producto, localidad)
            
            if resultados:
                st.success(f"Se encontraron {len(resultados)} posibles clientes en esa zona.")
                for lugar in resultados:
                    st.subheader(lugar.get("title", "Sin nombre comercial"))
                    
                    # NUEVO: Buscar y mostrar la foto de la fachada si está disponible
                    if "thumbnailUrl" in lugar:
                        # use_container_width adapta la foto al ancho del celular
                        st.image(lugar["thumbnailUrl"], use_container_width=True)
                    
                    st.write(f"📍 Dirección: {lugar.get('address', 'Dirección no disponible')}")
                    
                    if "phoneNumber" in lugar:
                        st.write(f"📞 Teléfono: {lugar['phoneNumber']}")
                        
                    st.write("---")
            else:
                st.warning("No se encontraron negocios con esos criterios en ese sector.")
    else:
        st.error("Por favor, ingresa el producto y el sector.")
