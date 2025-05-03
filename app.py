import datetime
import streamlit as st
import cv2
import numpy as np
import os
import re
import pandas as pd
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
from dotenv import load_dotenv
from validador import validar_cpf, validar_link_social

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Carrega variáveis do .env
load_dotenv()
POPPLER_PATH = os.getenv("dir_poppler")

data_nascimento_minima = datetime.date(1900, 1, 1)
data_nascimento_maxima = datetime.date.today()

# Função para pré-processar imagem
def preprocessar_imagem(img_np):
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    blur = cv2.medianBlur(gray, 3)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

# Função para validar documento com Tesseract
def validar_documento(documento, nome, cpf):
    try:
        if documento.name.endswith(".pdf"):
            imagens = convert_from_bytes(documento.read(), poppler_path=POPPLER_PATH)
            texto_extraido = ""
            for img in imagens:
                texto_extraido += pytesseract.image_to_string(img)
        else:
            img = Image.open(documento)
            img_np = np.array(img)
            img_processada = preprocessar_imagem(img_np)
            texto_extraido = pytesseract.image_to_string(img_processada)

        # Verificar se nome e CPF estão no texto extraído
        if not re.search(re.escape(nome), texto_extraido, re.IGNORECASE):
            return "Nome não encontrado no documento."
        if not re.search(re.escape(cpf), texto_extraido):
            return "CPF não encontrado no documento."
        return None  # Documento válido
    except Exception as e:
        return f"Erro ao validar documento: {str(e)}"

# App Streamlit
st.set_page_config(page_title="Know Your Fan", layout="centered")
st.title("Know Your Fan")
st.subheader("Cadastro de Fã de eSports")

with st.form("formulario_fan"):
    nome = st.text_input("👤 Nome completo")
    cpf = st.text_input("🆔 CPF")
    endereco = st.text_area("🏠 Endereço completo")
    data_nascimento = st.date_input("🎂 Data de nascimento",
                                    datetime.date(2000, 1, 1),
                                    min_value=data_nascimento_minima,
                                    max_value=data_nascimento_maxima,
                                    format="DD/MM/YYYY")
    instagram_url = st.text_input("📸 Link do Instagram")
    twitter_url = st.text_input("🐦 Link do Twitter")
    tiktok_url = st.text_input("♪ Link do TikTok") 
    interesses = st.text_area("🎮 Interesses em eSports (times, jogadores, modalidades etc.)")
    eventos = st.text_area("📅 Eventos que participou no último ano")
    compras = st.text_area("🛍️ Compras relacionadas a eSports (camisas, ingressos, etc.)")
    documento = st.file_uploader("📄 Upload de documento (RG ou CNH - Frente)", type=["jpg", "jpeg", "png", "pdf"])

    enviar = st.form_submit_button("Enviar")

def salvar_dados_csv(nome, cpf, data_nascimento, endereco, interesses, eventos, compras, arquivo_csv='dados_fas.csv'):
    novo_dado = {
        "Nome": nome,
        "CPF": cpf,
        "Data de Nascimento": data_nascimento.strftime("%d/%m/%Y"),
        "Endereço": endereco,
        "Interesses": interesses,
        "Eventos": eventos,
        "Compras": compras
    }

    try:
        df_existente = pd.read_csv(arquivo_csv)

        # Verifica se o CPF já está cadastrado
        if cpf in df_existente['CPF'].values:
            st.error("⚠️ Este CPF já está cadastrado.")
            return False  # sinaliza que não salvou

        df = pd.concat([df_existente, pd.DataFrame([novo_dado])], ignore_index=True)

    except FileNotFoundError:
        df = pd.DataFrame([novo_dado])

    df.to_csv(arquivo_csv, index=False)
    st.success("📝 Dados salvos com sucesso!")
    return True  # sinaliza que salvou


if enviar:
    st.success("✅ Dados recebidos!")
    st.write("👤 Nome:", nome)
    st.write("🆔 CPF:", cpf)
    st.write("🏠 Endereço:", endereco)
    st.write("🎂 Data de nascimento:", data_nascimento.strftime("%d/%m/%Y"))
    st.write("📸 Instagram:", instagram_url)
    st.write("🐦 Twitter:", twitter_url)
    st.write("♪ TikTok:", tiktok_url)
    st.write("🎮 Interesses:", interesses)
    st.write("📅 Eventos:", eventos)
    st.write("🛍️ Compras:", compras)
    
    erros = []

    if not nome.strip():
        erros.append("Nome não pode estar em branco.")

    if not validar_cpf(cpf):
        erros.append("CPF inválido.")

    for rede, url in [("Instagram", instagram_url), ("Twitter", twitter_url), ("TikTok", tiktok_url)]:
        if url and not validar_link_social(url):
            erros.append(f"Link do {rede} inválido.")

    if documento:
        erro_documento = validar_documento(documento, nome, cpf)
        if erro_documento:
            erros.append(erro_documento)
    else:
        erros.append("Documento não foi enviado.")

    if erros:
        for erro in erros:
            if erro != "Nome não encontrado no documento." and erro != "CPF não encontrado no documento.":
                st.error(erro)
            else:
                st.warning("⚠️ Validação de Nome e CPF no documento: funcionalidade inoperante utilizando ferramentas gratuitas.")
                st.success("🎉 Dados validados com sucesso!")
                if salvar_dados_csv(nome, cpf, data_nascimento, endereco, interesses, eventos, compras):
                    st.success("✅ Dados salvos com sucesso!")
                    st.balloons()

        