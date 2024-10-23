import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time
import os
from openpyxl.workbook import Workbook
import sqlite3
import pages.banco as banco


# Define o estilo CSS para os links
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
st.markdown(link_style, unsafe_allow_html=True)

# Função para buscar endereços por número do mapa
def buscar_enderecos_por_mapa(numero_mapa):
    c.execute("SELECT * FROM enderecos WHERE numero_mapa = ?", (numero_mapa,))
    return c.fetchall()

# Conectando ao banco de dados SQLite
conn = sqlite3.connect('enderecos_mapas.db')
c = conn.cursor()

# Criando a tabela de endereços se não existir
c.execute('''CREATE TABLE IF NOT EXISTS enderecos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,   
                  numero_mapa TEXT,
                  numero_endereco TEXT,
                  sexo TEXT, 
                  nome TEXT, 
                  latitude REAL, 
                  longitude REAL)''')
conn.commit()

with st.spinner('Espere um pouco...'):
    time.sleep(0.5)

# Cria um título para o aplicativo
st.title("Mapas Congregação Ls Progresso")

# Coordenadas iniciais do mapa
coordenadas_iniciais = [-19.912998, -43.940933]  # Minas Gerais

# Verifica se o arquivo Excel já existe
if os.path.exists("dados_mapa.xlsx"):
    df_existente = pd.read_excel("dados_mapa.xlsx")
else:
    df_existente = pd.DataFrame(columns=["Data", "Observação", "Mapa Selecionado"])

st.subheader("Escolha o Mapa desejado:")
mapa_selecionado = st.number_input("Selecione o número do mapa", min_value=1, step=1, max_value=93)

# Barra lateral para selecionar o número do mapa e informações adicionais
with st.sidebar:
    st.logo(image="images/libras.png",icon_image="images/libras.png")
    
    
    data_hoje = st.date_input("Escolha a data", format= "DD/MM/YYYY")
    text = st.text_input("Número do endereço a ser atualizado:")
    atualizacao = st.selectbox("Atualização", ["Encontrado", "Não encontrado", "Falei com a Família", "Mudou-se", "Inexistente"])

    # Buscar e exibir endereços associados ao mapa
    enderecos = buscar_enderecos_por_mapa(mapa_selecionado)

 
    
    if st.button('Enviar'):
        # Cria um DataFrame com as novas informações
        df_novo = pd.DataFrame({
            "Data": [data_hoje],
            "Número endereço": [text],
            "Mapa Selecionado": [mapa_selecionado],
            "Atualização": [atualizacao]
        })

        # Concatena os dados existentes com os novos dados
        df_atualizado = pd.concat([df_existente, df_novo], ignore_index=True)

        # Salva em uma planilha Excel
        df_atualizado.to_excel("dados_mapa.xlsx", index=False)
        st.success("Dados salvos com sucesso!")
    st.text("")
    st.text("")



# Cria o mapa com as coordenadas iniciais
mapa_interativo = folium.Map(location=coordenadas_iniciais, zoom_start=13)

# Adiciona os marcadores ao mapa
for endereco in enderecos:
    id_endereco, numero_mapa, numero_endereco, sexo, nome, latitude, longitude = endereco
    folium.Marker(
        location=[latitude, longitude],
        popup=nome,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mapa_interativo)

# Exibe o mapa interativo no Streamlit
st_data = st_folium(mapa_interativo, width=725, height=400)



# Exibe os endereços como links para o Google Maps
# Função para gerar links do Google Maps para cada endereço
def gerar_link_google_maps(latitude, longitude):
    return f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

# Exibe os endereços como uma tabela com links
st.subheader("Endereços no Google Maps")

# Cria uma lista de dicionários para cada endereço, incluindo o link formatado
enderecos_dados = []
for endereco in enderecos:
    id_endereco, numero_mapa, numero_endereco, sexo, nome, latitude, longitude = endereco
    link = gerar_link_google_maps(latitude, longitude)
    enderecos_dados.append({
        "Número do Endereço": numero_endereco,
        "Sexo": sexo,
        "Endereços": nome,
        "Google Mapas": f'<a href="{link}" target="_blank">Ir para o Maps</a>'
    })

# Converte a lista de dicionários para um DataFrame
df_enderecos = pd.DataFrame(enderecos_dados)

# Define o estilo CSS para melhorar a aparência da tabela
table_style = """
<style>
table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

th, td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

th {
    font-weight: bold;
}

tr:hover {background-color: #f5f5f5;}
a {
    color: blue;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
"""

# Exibe o estilo e a tabela como HTML com links clicáveis
st.markdown(table_style, unsafe_allow_html=True)
st.markdown(df_enderecos.to_html(escape=False, index=False), unsafe_allow_html=True)
