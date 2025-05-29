import streamlit as st
import requests
import time

# 🔑 Substitua pela sua chave da OpenCage
OPENCAGE_KEY = "6fee265fdab948b1a1d740bead306441"

st.set_page_config(page_title="Geocodificação Reversa com OpenCage", layout="centered")
st.title("🔁 Geocodificação Reversa com OpenCage")
st.write("Digite as coordenadas (latitude,longitude), uma por linha:")

entrada = st.text_area("Coordenadas", height=200)

# 🔘 Seleção de quais campos exibir
st.markdown("### 🛠️ Selecione quais partes do endereço deseja exibir:")
exibir_rua = st.checkbox("Rua", value=True)
exibir_bairro = st.checkbox("Bairro", value=True)
exibir_cidade = st.checkbox("Cidade", value=True)

if st.button("Buscar Endereços"):
    linhas = entrada.strip().split("\n")
    total = len(linhas)
    resultados = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, linha in enumerate(linhas, 1):
        try:
            lat_str, lon_str = linha.split(",")
            lat, lon = float(lat_str.strip()), float(lon_str.strip())

            url = "https://api.opencagedata.com/geocode/v1/json"
            params = {
                'q': f"{lat},{lon}",
                'key': OPENCAGE_KEY,
                'language': 'pt',
                'pretty': 1
            }

            response = requests.get(url, params=params)
            time.sleep(1.5)

            if response.status_code == 200:
                data = response.json()
                if data["results"]:
                    comp = data["results"][0]["components"]

                    partes = []
                    if exibir_rua:
                        partes.append(comp.get("road", ""))
                    if exibir_bairro:
                        partes.append(comp.get("suburb", "") or comp.get("neighbourhood", ""))
                    if exibir_cidade:
                        partes.append(comp.get("city", "") or comp.get("town", "") or comp.get("village", ""))

                    endereco = ", ".join([p for p in partes if p]) + "."
                else:
                    endereco = "Endereço não encontrado."
            elif response.status_code == 429:
                endereco = f"Erro 429: Limite de requisições atingido. Tente novamente em alguns minutos."
            else:
                endereco = f"Erro {response.status_code}"

            resultados.append(f"{i}. {endereco}")
        except Exception as e:
            resultados.append(f"{i}. Erro: {str(e)}")

        progress_bar.progress(i / total)
        status_text.text(f"Processando {i}/{total} coordenadas...")

    st.markdown("### 📍 Endereços Encontrados:")
    for r in resultados:
        st.write(r)

    status_text.text("✅ Processamento concluído!")

