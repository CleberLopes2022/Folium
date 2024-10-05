import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time
import os
from openpyxl.workbook import Workbook

# Define the CSS style
link_style = """
<style>
a {
    color: blue; /* Mude a cor do texto aqui */
    text-decoration: none; /* Remove sublinhado, se desejar */
}
a:hover {
    color: blue; /* Cor quando o mouse está sobre o link */
}
</style>
"""

with st.spinner('Espere um pouco...'):
    time.sleep(0.5)

# Cria um título para o aplicativo
st.title("Mapas Congregação Ls Progresso")

# Coordenadas iniciais do mapa
coordenadas_iniciais = [-19.912998, -43.940933]  # Minas Gerais

# Lista de endereços com suas coordenadas (latitude, longitude)
mapa1 = [
    {"numero": "1 -","sexo": " H  ","nome": "Rua Capitão Gustavo Murgel, 399 - Alto Caiçara", "coordenadas": [-19.908687, -43.972579]},
    {"numero": "2 -","sexo": " C  ","nome": "Rua Manhumirim, 1384 - Pedro II", "coordenadas": [-19.9057534,-43.9721629]},
    {"numero": "3 -","sexo": " C ","nome": "Rua Padre Eustáquio, 1918 - Padre Eustáquio", "coordenadas": [-19.9148484,-43.9732229]}
]

mapa2 = [
    {"numero": "4 -","sexo": "M ","nome": "Rua Álvaro Alvim, 10 - Vila Amaral", "coordenadas": [-19.8926297,-43.9749863]},
    {"numero": "5 -","sexo": "M ","nome": "Rua Rua Professor Francisco Henrique, 220 - Alto Caiçara", "coordenadas": [-19.8969632,-43.9794049]},
    {"numero": "6 -","sexo": "H ","nome": "Rua Rua Casuarina, 108 - Caiçara", "coordenadas": [-19.8995596,-43.9816526]},
    {"numero": "7 -","sexo": "M ","nome": "Rua Bangu, 177 1º andar - Caiçara", "coordenadas": [-19.901425,-43.9795171]}
]

mapa3 = [
    {"numero": "8 -","sexo": "C ","nome": "Rua Henrique Gorceix, 1780A(Surdo Cego) - Monsenhor Messias", "coordenadas": [-19.9087352,-43.9817311]},
    {"numero": "9 -","sexo": "C ","nome": "Rua Henrique Gorceix, 1780 - Monsenhor Messias", "coordenadas": [-19.9087352,-43.9817311]},
    {"numero": "10 -","sexo": "H ","nome": "Av. Pandiá Calógeras, 52 D - Monsenhor Messias", "coordenadas": [-19.9026122,-43.9848326]},
    {"numero": "11 -","sexo": "M ","nome": "Rua Leopoldo Pereira, 406 - Monsenhor Messias", "coordenadas": [-19.9037142,-43.9840333]}
]

# Mapeamento dos nomes dos mapas para os dados de coordenadas
mapas_opcoes = {
    "mapa1": mapa1,
    "mapa2": mapa2,
    "mapa3": mapa3
}


if 'observacao' not in st.session_state:
    st.session_state['observacao'] = ""


# Verifica se o arquivo Excel já existe
if os.path.exists("dados_mapa.xlsx"):
    df_existente = pd.read_excel("dados_mapa.xlsx")
else:
    df_existente = pd.DataFrame(columns=["Data", "Observação", "Mapa Selecionado"])

with st.sidebar:
    st.image("libras.png", width=200)
    st.title("Escolha o Mapa desejado :")
    mapa_selecionado = st.selectbox("Mapas", ["mapa1", "mapa2", "mapa3"])
    data_hoje = st.date_input("Escolha a data")
    text = st.text_input("Numero do endereço a ser atualizado: ")
    atualizacao = st.selectbox("Atualização", ["Encontrado","Não_encontrado","Falei com a Família","mudou-se","Inexistente"])
   
  

    if st.button('Enviar'):
        # Cria um DataFrame com as novas informações
        df_novo = pd.DataFrame({
            "Data": [data_hoje],
            "Numero endereco": [text],
            "Mapa Selecionado": [mapa_selecionado],
            "Atualizacao": [atualizacao]
        })

        # Concatena os dados existentes com os novos dados
        df_atualizado = pd.concat([df_existente, df_novo], ignore_index=True)

        # Salva em uma planilha Excel
        df_atualizado.to_excel("dados_mapa.xlsx", index=False)
        st.success("Dados salvos com sucesso!")


# Recupera o mapa selecionado
enderecos = mapas_opcoes[mapa_selecionado]

# Cria o mapa com as coordenadas iniciais
mapa_interativo = folium.Map(location=coordenadas_iniciais, zoom_start=13)

# Adiciona os marcadores ao mapa
for endereco in enderecos:
    folium.Marker(
        location=endereco["coordenadas"],
        popup=endereco["nome"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mapa_interativo)

# Exibe o mapa interativo no Streamlit
st_data = st_folium(mapa_interativo, width=725, height=400)

# Exibe os endereços como links para o Google Maps
st.subheader("Endereços no Google Maps")
for endereco in enderecos:
    lat, lon = endereco["coordenadas"]
    link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    st.markdown(f"[{endereco['numero']},{endereco['sexo']},{endereco['nome']}]({link})")

#  --------------------------------------------------------------------------------

