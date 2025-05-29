import streamlit as st
import googlemaps
import time

# Pega a chave da API Google dos Secrets do Streamlit
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Cria cliente do Google Maps
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

st.title("Geocodificação reversa com Google Maps API")

# Campo para digitar latitudes e longitudes separados por vírgula ou linha
input_text = st.text_area("Cole latitudes e longitudes (ex: -5.9396,-35.2512)", height=150)

if st.button("Buscar endereços"):

    if not input_text.strip():
        st.error("Por favor, insira pelo menos uma latitude e longitude.")
    else:
        # Processa as linhas
        coords_list = input_text.strip().split('\n')
        total = len(coords_list)

        for i, coord in enumerate(coords_list, start=1):
            st.write(f"{i}/{total}")
            try:
                lat_str, lng_str = coord.split(",")
                lat = float(lat_str.strip())
                lng = float(lng_str.strip())

                # Faz geocodificação reversa usando Google Maps API
                results = gmaps.reverse_geocode((lat, lng))

                if results:
                    # Pega o endereço formatado do primeiro resultado
                    address = results[0]["formatted_address"]

                    # Se aparecer "Unnamed Road", substitui por "Rua sem nome"
                    if "Unnamed Road" in address:
                        address = address.replace("Unnamed Road", "Rua sem nome")

                    st.write(f"{i}. {address}")

                else:
                    st.write(f"{i}. Endereço não encontrado para: {lat}, {lng}")

            except Exception as e:
                st.write(f"{i}. Erro ao processar: {coord} - {e}")

            # Pequena pausa para evitar limite de requisições (Rate Limit)
            time.sleep(1)
