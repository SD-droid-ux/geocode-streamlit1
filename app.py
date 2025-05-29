import streamlit as st
import googlemaps
import time

# Pega a chave da API Google dos Secrets do Streamlit
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Cria cliente do Google Maps
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

st.title("Geocodificação reversa com Google Maps API")

# Checkbox para o usuário escolher o que mostrar
show_street = st.checkbox("Rua", value=True)
show_neighborhood = st.checkbox("Bairro", value=True)
show_city = st.checkbox("Cidade", value=True)

# Campo para digitar latitudes e longitudes separados por vírgula ou linha
input_text = st.text_area("Cole latitudes e longitudes (ex: -5.9396,-35.2512)", height=150)

if st.button("Buscar endereços"):

    if not input_text.strip():
        st.error("Por favor, insira pelo menos uma latitude e longitude. Separe Latitude e Longitude com Vírgula (Exemplo: -23.92, -47.07)")
    else:
        coords_list = input_text.strip().split('\n')
        total = len(coords_list)

        progress_bar = st.progress(0)

        for i, coord in enumerate(coords_list, start=1):
            try:
                lat_str, lng_str = coord.split(",")
                lat = float(lat_str.strip())
                lng = float(lng_str.strip())

                results = gmaps.reverse_geocode((lat, lng))

                if results:
                    address_components = results[0]["address_components"]

                    # Extrair partes do endereço
                    street = bairro = cidade = ""

                    for comp in address_components:
                        types = comp["types"]
                        if "route" in types:
                            street = comp["long_name"]
                        if "sublocality" in types or "neighborhood" in types:
                            bairro = comp["long_name"]
                        if "locality" in types:
                            cidade = comp["long_name"]

                    # Ajusta rua sem nome
                    if street == "" or street.lower() == "unnamed road":
                        street = "Rua sem nome"

                    # Monta a resposta conforme seleção do usuário
                    parts = []
                    if show_street and street:
                        parts.append(street)
                    if show_neighborhood and bairro:
                        parts.append(bairro)
                    if show_city and cidade:
                        parts.append(cidade)

                    display_address = ", ".join(parts)
                    if display_address == "":
                        display_address = results[0]["formatted_address"]

                    st.write(f"{i}. {display_address}")

                else:
                    st.write(f"{i}. Endereço não encontrado para: {lat}, {lng}")

            except Exception as e:
                st.write(f"{i}. Erro ao processar: {coord} - {e}")

            # Atualiza barra de progresso
            progress_bar.progress(i / total)

            time.sleep(1)
