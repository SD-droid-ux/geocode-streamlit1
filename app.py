import streamlit as st
import requests
import time

# --- IMAGEM DE FUNDO ---
imagem_fundo_url = "https://drive.google.com/uc?export=view&id=1epeU9Mvsqk29YtQZY96IaLSQtoEIgeXf"

pagina_fundo = f"""
<style>
    .stApp {{
        background-image: url("{imagem_fundo_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
</style>
"""

st.markdown(pagina_fundo, unsafe_allow_html=True)

# --- TÍTULO E ENTRADA ---
st.title("Conversor de Coordenadas para Endereço")
coordenadas_input = st.text_area("Insira as coordenadas (uma por linha):", height=200)
api_key = st.secrets["6fee265fdab948b1a1d740bead306441"] if "6fee265fdab948b1a1d740bead306441" in st.secrets else st.text_input("Sua chave API do OpenCage", type="password")

# --- FUNÇÃO DE BUSCA ---
def buscar_endereco(lat, lon):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={api_key}&language=pt&pretty=1"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        if dados["results"]:
            endereco_completo = dados["results"][0]["formatted"]
            if "unnamed road" in endereco_completo.lower():
                endereco_completo = endereco_completo.replace("unnamed road", "rua sem nome").replace("Unnamed Road", "rua sem nome")
            partes = endereco_completo.split(",")
            resumo = ", ".join(partes[:6]).strip()
            return resumo
    return "Endereço não encontrado"

# --- BOTÃO DE PROCESSAMENTO ---
if st.button("Buscar Endereços"):
    linhas = coordenadas_input.strip().split("\n")
    total = len(linhas)
    resultados = []
    barra = st.empty()

    for i, linha in enumerate(linhas, 1):
        if "," in linha:
            try:
                lat, lon = map(str.strip, linha.split(","))
                endereco = buscar_endereco(lat, lon)
                resultados.append(f"{i}. {endereco}")
            except:
                resultados.append(f"{i}. Erro ao processar: {linha}")
        else:
            resultados.append(f"{i}. Formato inválido: {linha}")

        barra.text(f"{i}/{total}")
        time.sleep(1)  # Evita erro 429 (muitos pedidos por segundo)

    st.subheader("Endereços encontrados:")
    for linha in resultados:
        st.write(linha)




