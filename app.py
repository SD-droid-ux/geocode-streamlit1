import streamlit as st
import googlemaps

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)


st.set_page_config(page_title="Geocodificador Google", layout="centered")

st.markdown("## 🗺️ Conversor de Latitude/Longitude para Endereço (Google Maps API)")

lat_lng_input = st.text_area("Insira as coordenadas (uma por linha no formato LAT, LNG):")

if st.button("Buscar endereços"):
    coordenadas = [linha.strip() for linha in lat_lng_input.strip().split("\n") if linha.strip()]
    
    if not coordenadas:
        st.warning("Por favor, insira pelo menos uma coordenada.")
    else:
        resultados = []
        total = len(coordenadas)
        
        with st.spinner("Buscando endereços..."):
            for i, coord in enumerate(coordenadas, 1):
                try:
                    lat, lon = map(str.strip, coord.split(","))
                    lat, lon = float(lat), float(lon)

                    resultado = gmaps.reverse_geocode((lat, lon), language="pt-BR")
                    if resultado:
                        endereco = resultado[0]["formatted_address"]
                        if "Unnamed Road" in endereco:
                            endereco = endereco.replace("Unnamed Road", "rua sem nome")
                        partes = endereco.split(",")
                        resumo = ", ".join(partes[:6]).strip()
                    else:
                        resumo = "Endereço não encontrado"

                except Exception as e:
                    resumo = f"Erro: {str(e)}"

                resultados.append(f"{i}. {resumo}")
                st.markdown(f"🔄 {i}/{total}")
                time.sleep(1)  # Respeita o rate limit da API

        st.success("Busca finalizada!")
        st.markdown("### 📍 Endereços encontrados:")
        for r in resultados:
            st.markdown(r)
