import streamlit as st
import requests
import time

# Título do app
st.title("Conversor de Coordenadas para Endereço")

# Chave da API do OpenCage
API_KEY = "6fee265fdab948b1a1d740bead306441"

# Caixa de seleção de partes do endereço
st.subheader("Escolha o que deseja exibir:")
mostrar_rua = st.checkbox("Rua", value=True)
mostrar_bairro = st.checkbox("Bairro", value=True)
mostrar_cidade = st.checkbox("Cidade", value=True)

# Entrada de coordenadas
st.subheader("Digite as coordenadas (uma por linha):")
coords_text = st.text_area("Formato: latitude, longitude", height=200)

# Função que faz a requisição para o OpenCage
def geocode(lat, lon):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat},{lon}&key={API_KEY}&language=pt"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            comp = data['results'][0]['components']
            partes = []
            if mostrar_rua:
                partes.append(comp.get('road', ''))
            if mostrar_bairro:
                partes.append(comp.get('suburb', '') or comp.get('neighbourhood', ''))
            if mostrar_cidade:
                partes.append(comp.get('city', '') or comp.get('town', '') or comp.get('village', ''))
            return ", ".join([p for p in partes if p])
    return "Endereço não encontrado"

# Quando o botão é clicado
if st.button("Buscar endereços"):
    coords = coords_text.strip().split("\n")
    resultados = []
    with st.spinner("Buscando endereços..."):
        for i, linha in enumerate(coords):
            lat_lon = linha.split(",")
            if len(lat_lon) != 2:
                resultados.append(f"{i+1}. Entrada inválida")
                continue
            lat, lon = lat_lon[0].strip(), lat_lon[1].strip()
            resultado = geocode(lat, lon)
            resultados.append(f"{i+1}. {resultado}")
            time.sleep(1.1)  # evita erro 429 (limite de requisições)

    st.subheader("Resultados:")
    for r in resultados:
        st.write(r)

