import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time
import os
import sqlite3

# Configuração da Página
st.set_page_config(page_title="Ls Maps", page_icon="Images/ls2.png", layout="wide")

# Adicionando o logo
st.logo(image="Images/libras.png", icon_image="Images/libras.png")

# Define o estilo CSS para os links e tabelas
link_style = """
<style>
a {
    color: blue;
    text-decoration: none;
}
a:hover {
    color: blue;
}
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
</style>
"""
st.markdown(link_style, unsafe_allow_html=True)

# Conexão ao banco de dados SQLite
conn = sqlite3.connect('enderecos_mapas.db')
c = conn.cursor()

# Cria a tabela no banco, se não existir
c.execute('''CREATE TABLE IF NOT EXISTS enderecos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,   
              numero_mapa TEXT,
              numero_endereco TEXT,
              sexo TEXT, 
              nome TEXT, 
              latitude REAL, 
              longitude REAL)''')
conn.commit()

# Função para buscar endereços por número do mapa
def buscar_enderecos_por_mapa(numero_mapa):
    c.execute("SELECT * FROM enderecos WHERE numero_mapa = ?", (numero_mapa,))
    return c.fetchall()

# Configuração Inicial da Interface
with st.spinner('Espere um pouco...'):
    time.sleep(0.5)

st.title("Mapas Congregação Ls Progresso")
st.write("-----")
st.subheader("Escolha o Mapa desejado:")

# Barra lateral para seleção do mapa
mapa_selecionado = st.number_input("Selecione o número do mapa", min_value=0, step=1, max_value=93)

# Coordenadas padrão
coordenadas_iniciais = [-19.912998, -43.940933]  # Minas Gerais
localidade = ""

# Lógica para definir a localidade e coordenadas iniciais com base no mapa selecionado
if mapa_selecionado in [1, 2]:
    localidade = "Alto Caiçaras"
elif mapa_selecionado == 3:
    localidade = "Monsenhor Messias"
elif mapa_selecionado in [5, 6, 7]:
    coordenadas_iniciais = [-19.914338, -43.9911932]
    localidade = "Padre Eustáquio"
elif mapa_selecionado == 8:
    coordenadas_iniciais = [-19.9135286, -43.9669018]
    localidade = "Carlos Prates"
elif mapa_selecionado in [10, 11, 12, 13]:
    coordenadas_iniciais = [-19.9344036, -44.0000137]
    localidade = "Gameleira"
# (Adicione o resto das condições conforme necessário...)

# Exibe a informação do cartão de território
st.write("-----")
st.subheader("Cartão Mapa de Território")
st.write(" Localidade: **", localidade, "** | __Território Nº:__", mapa_selecionado)

# Buscar e exibir endereços do banco de dados
enderecos = buscar_enderecos_por_mapa(mapa_selecionado)

# Mapas Interativos
if 0 < mapa_selecionado <= 93:
    # Criação do mapa interativo
    mapa_interativo = folium.Map(location=coordenadas_iniciais, zoom_start=13)

    # Adiciona os marcadores no mapa
    for endereco in enderecos:
        _, _, numero_endereco, sexo, nome, latitude, longitude = endereco
        folium.Marker(
            location=[latitude, longitude],
            popup=f"{nome} - {sexo}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(mapa_interativo)

    # Exibe o mapa no Streamlit
    st_data = st_folium(mapa_interativo, width=800, height=450)
    time.sleep(1.5)

# Tabela de Endereços com Links
st.subheader("Endereços no Google Maps e Waze")
enderecos_dados = []
enderecos_para_rota = []  # Lista para armazenar os endereços da rota completa

for endereco in enderecos:
    _, _, numero_endereco, sexo, nome, _, _ = endereco  # Ignorando latitude e longitude

    # Substitui espaços no endereço para links
    endereco_formatado = nome.replace(' ', '+')
    google_maps_link = f"https://www.google.com/maps/search/{endereco_formatado}"
    waze_link = f"https://waze.com/ul?q={endereco_formatado}&navigate=yes"

    # Adiciona o endereço formatado à lista de rotas
    enderecos_para_rota.append(endereco_formatado)

    enderecos_dados.append({
        "Número do Endereço": numero_endereco,
        "Sexo": sexo,
        "Endereço": nome,
        "Google Maps": f'<a href="{google_maps_link}" target="_blank">Abrir no Google Maps</a>',
        "Waze": f'<a href="{waze_link}" target="_blank">Abrir no Waze</a>'
    })

# Exibe os endereços em uma tabela interativa
df_enderecos = pd.DataFrame(enderecos_dados)
if not df_enderecos.empty:
    st.markdown(df_enderecos.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Criação do link para rota completa
    if len(enderecos_para_rota) > 1:
        # Junta os endereços formatados para criar a rota
        google_maps_rota = f"https://www.google.com/maps/dir/" + "/".join(enderecos_para_rota)
        waze_rota = f"https://waze.com/ul?ll={enderecos_para_rota[0]}&navigate=yes&q=" + "|".join(enderecos_para_rota)

        # Exibe os links para a rota completa
        st.subheader("Rota Completa")
        st.markdown(f'📍 **Google Maps**: [Clique aqui para abrir a rota completa no Google Maps]({google_maps_rota})', unsafe_allow_html=True)
        st.markdown(f'🚗 **Waze**: [Clique aqui para abrir a rota completa no Waze]({waze_rota})', unsafe_allow_html=True)
else:
    st.warning("Nenhum endereço encontrado para este mapa.")
