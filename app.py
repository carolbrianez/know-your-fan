import streamlit as st
import cv2
import numpy as np
import os
import easyocr
import re
from PIL import Image
from pdf2image import convert_from_bytes
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
POPPLER_PATH = os.getenv("dir_poppler")

# Inicializa EasyOCR
reader = easyocr.Reader(['pt'], gpu=False)

# Função para extrair texto com EasyOCR
def extrair_texto_easyocr(img_np):
    results = reader.readtext(img_np)
    texto = "\n".join([res[1] for res in results])
    return texto

# Função para pré-processar imagem
def preprocessar_imagem(img_np):
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    blur = cv2.medianBlur(gray, 3)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

# App Streamlit
st.set_page_config(page_title="Know Your Fan", layout="centered")
st.title("Know Your Fan")
st.subheader("Cadastro de Fã de eSports")

with st.form("formulario_fan"):
    nome = st.text_input("👤 Nome completo")
    cpf = st.text_input("🆔 CPF")
    endereco = st.text_area("🏠 Endereço completo")
    interesses = st.text_area("🎮 Interesses em eSports (times, jogadores, modalidades etc.)")
    eventos = st.text_area("📅 Eventos que participou no último ano")
    compras = st.text_area("🛍️ Compras relacionadas a eSports (camisas, ingressos, etc.)")
    documento = st.file_uploader("📄 Upload de documento (RG ou CNH - Frente)", type=["jpg", "jpeg", "png", "pdf"])

    enviar = st.form_submit_button("Enviar")

if enviar:
    st.success("✅ Dados recebidos!")
    st.write("👤 Nome:", nome)
    st.write("🆔 CPF:", cpf)
    st.write("🏠 Endereço:", endereco)
    st.write("🎮 Interesses:", interesses)
    st.write("📅 Eventos:", eventos)
    st.write("🛍️ Compras:", compras)

    if documento:
        st.write("📄 Documento enviado com sucesso!")
        imagem = None

        if documento.type == "application/pdf":
            st.info("📄 Convertendo PDF em imagem para leitura...")
            documento.seek(0)
            imagens = convert_from_bytes(documento.read(), dpi=300, poppler_path=POPPLER_PATH)
            imagem = np.array(imagens[0])
        else:
            file_bytes = np.asarray(bytearray(documento.read()), dtype=np.uint8)
            imagem = cv2.imdecode(file_bytes, 1)

        if imagem is not None:
            imagem_pre = preprocessar_imagem(imagem)
            st.info("🔍 Extraindo texto com EasyOCR...")
            texto = extrair_texto_easyocr(imagem_pre)

            st.subheader("📄 Texto extraído do documento:")
            st.text(texto)

            # Validar nome
            nome_valido = nome.lower() in texto.lower()

            # Validar CPF via regex
            cpf_regex = re.search(r'\d{3}[\.\s]?\d{3}[\.\s]?\d{3}[\-]?\d{2}', texto)
            cpf_encontrado = cpf_regex.group().replace(".", "").replace("-", "") if cpf_regex else ""

            cpf_valido = cpf.replace(".", "").replace("-", "") == cpf_encontrado

            if nome_valido and cpf_valido:
                st.success("✅ Nome e CPF conferem com o documento.")
            else:
                st.warning("⚠️ Nome ou CPF não foram encontrados corretamente.")
                if not nome_valido:
                    st.write("🔍 Nome não localizado.")
                if not cpf_valido:
                    st.write(f"🔍 CPF extraído: `{cpf_encontrado or 'não identificado'}`")
    else:
        st.warning("⚠️ Nenhum documento enviado.")
