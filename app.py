import streamlit as st
import requests
import time

st.title("Conversor de Coordenadas para Endereço")

# Coloque aqui sua chave API do OpenCage
API_KEY = "6fee265fdab948b1a1d740bead306441"

def geocode(lat, lon):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat},{lon}&key={API_KEY}&language=pt"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            comp = data['results'][0]['components']
            rua = comp.get('road', '')
            bairro = comp.get('suburb', '') or comp.get('neighbourhood', '')
            cidade = comp.get('city', '') or comp.get('town', '') or comp.get('village', '')
            return f"{rua}, {bairro}, {cidade}"
    return "Endereço não encontrado"

coords_text = st.text_area("Digite as coordenadas (lat, lon), uma por linha")

if st.button("Buscar endereços"):
    coords = coords_text.strip().split("\n")
    resultados = []
    for i, linha in enumerate(coords):
        lat_lon = linha.split(",")
        if len(lat_lon) != 2:
            resultados.append(f"{i+1}. Entrada inválida")
            continue
        lat, lon = lat_lon[0].strip(), lat_lon[1].strip()
        resultado = geocode(lat, lon)
        resultados.append(f"{i+1}. {resultado}")
        time.sleep(1.1)  # evita limite de requisições

    for r in resultados:
        st.write(r)


