import streamlit as st
from app import mapa_selecionado
import pandas as pd
import os

st.set_page_config(page_title="Ls Maps", page_icon="Images/ls2.png", layout="wide")

st.logo(image="Images/libras.png", icon_image="Images/libras.png")


st.title("Atualização dos endereços")


data_hoje = st.date_input("Escolha a data", format="DD/MM/YYYY")
mapa_selecionado1 = st.number_input("Selecione o número do mapa", min_value=0, step=1, max_value=93)
text = st.number_input("Numero do Endereço: ", min_value=0, step=1, max_value=10)
atualizacao = st.selectbox("Atualização", ["Encontrado", "Não encontrado", "Falei com a Família", "Mudou-se", "Inexistente"])


if st.button('Enviar'):
        # Cria um DataFrame com as novas informações
    df_novo = pd.DataFrame({
            "Data": [data_hoje],
            "Número endereço": [text],
            "Mapa Selecionado": [mapa_selecionado1],
            "Atualização": [atualizacao]
        })

        # Verifica se o arquivo Excel já existe
    if os.path.exists("dados_mapa.xlsx"):
            df_existente = pd.read_excel("dados_mapa.xlsx")
    else:
            df_existente = pd.DataFrame(columns=["Data", "Mapa Selecionado","Número endereço", "Atualização"])

        # Concatena os dados existentes com os novos dados
    df_atualizado = pd.concat([df_existente, df_novo], ignore_index=True)

        # Salva em uma planilha Excel
    df_atualizado.to_excel("dados_mapa.xlsx", index=False)
    st.success("Dados salvos com sucesso!")


df = pd.read_excel("dados_mapa.xlsx")

st.dataframe(df.tail(10),use_container_width=True)

df = pd.read_excel("dados_mapa.xlsx")

st.dataframe(df.tail(10))
