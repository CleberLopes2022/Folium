import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time
import os
import sqlite3


# Configuração do Layout da página

st.set_page_config(page_title="Ls Maps", page_icon="Images/ls2.png", layout="wide")

st.logo(image="Images/libras.png", icon_image="Images/libras.png")

# Define o estilo CSS para os links

link_style = """
<style>
a {
    color: blue;
    text-decoration: none;
}
a:hover {
    color: blue;
}
</style>
"""
st.markdown(link_style, unsafe_allow_html=True)


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

# Função para buscar endereços por número do mapa
def buscar_enderecos_por_mapa(numero_mapa):
    c.execute("SELECT * FROM enderecos WHERE numero_mapa = ?", (numero_mapa,))
    return c.fetchall()

with st.spinner('Espere um pouco...'):
    time.sleep(0.5)

# Cria um título para o aplicativo
st.title("Mapas Congregação Ls Progresso")
st.write("-----")

# Coordenadas iniciais do mapa

coordenadas_iniciais = [-19.912998, -43.940933]  # Minas Gerais
localidade = ""

st.session_state.mapa_selecionado = None  

st.subheader("Escolha o Mapa desejado:")
mapa_selecionado = st.number_input("Selecione o número do mapa", min_value=0, step=1, max_value=93)

if mapa_selecionado == 1 or mapa_selecionado == 2:
    localidade = "Alto Caiçaras"
elif mapa_selecionado == 3:
    localidade = "Monsenhor Messias"
elif mapa_selecionado == 4:
    localidade = "Santo André"
elif mapa_selecionado == 5 or mapa_selecionado == 6 or mapa_selecionado == 7:
    coordenadas_iniciais = [-19.914338,-43.9911932]  # Padre Eustáquio
    localidade = "Padre Eustáquio"
elif mapa_selecionado == 8:
    coordenadas_iniciais = [-19.9135286, -43.9669018]
    localidade = "Carlos Prates"
elif mapa_selecionado == 9:
    coordenadas_iniciais = [-19.9246934, -43.9939625]
    localidade = "Coração Eucarístico"
elif mapa_selecionado == 10 or mapa_selecionado == 11 or mapa_selecionado == 12 or mapa_selecionado == 13:
    coordenadas_iniciais = [-19.9344036, -44.0000137]  #Gameleira
    localidade = "Gameleira"
elif mapa_selecionado == 14 or mapa_selecionado == 15 or mapa_selecionado == 16 or mapa_selecionado == 17 or mapa_selecionado == 18 or mapa_selecionado == 19 or mapa_selecionado == 20:
    coordenadas_iniciais = [-19.911415, -44.0319767]
    localidade = "Pindorama"
elif mapa_selecionado == 21 or mapa_selecionado == 23 or mapa_selecionado == 25:
    coordenadas_iniciais = [-19.8965993, -44.0148256]
    localidade = "Alipio de Melo"
elif mapa_selecionado == 27:
    coordenadas_iniciais = [-19.8767773, -44.0049155]
    localidade = " Ouro Preto"
elif mapa_selecionado == 28 or mapa_selecionado == 29 or mapa_selecionado == 30 or mapa_selecionado == 31 or mapa_selecionado == 32:
    coordenadas_iniciais = [-19.8716564, -44.0113555]
    localidade= "Santa Terezinha/Serrano"
elif mapa_selecionado == 33 or mapa_selecionado == 34 or mapa_selecionado == 35:
    coordenadas_iniciais = [-19.8646894,-44.0286357]
    localidade = "Estrela Dalva"
elif mapa_selecionado == 36 or  mapa_selecionado == 37 or mapa_selecionado == 39 or mapa_selecionado == 40 or mapa_selecionado == 41 or mapa_selecionado == 42 or mapa_selecionado == 43:
    coordenadas_iniciais = [-19.8456058,-44.0336325]  # Nacional
    localidade = "Nacional"
elif mapa_selecionado == 44:
    coordenadas_iniciais = [-19.9337304, -43.9826117]
    localidade = "Calafate"
elif mapa_selecionado == 45 or mapa_selecionado == 46:
    coordenadas_iniciais = [-19.9239335,-43.9745692]
    localidade = "Prado"
elif mapa_selecionado == 47 or mapa_selecionado == 48:
    coordenadas_iniciais = [-19.8942484,-43.9724828]
    localidade = "Aparecida"
elif mapa_selecionado == 49 or mapa_selecionado == 50:
    coordenadas_iniciais = [-19.8779747,-43.9605378]
    localidade = "Santa Cruz"
elif mapa_selecionado == 51:
    coordenadas_iniciais = [-19.8779747,-43.9605378]
    localidade = "Renascença"
elif mapa_selecionado == 53:
    coordenadas_iniciais = [-19.8779747,-43.9605378]
elif mapa_selecionado == 54:
    coordenadas_iniciais = [-19.8779747,-43.9605378]
    localidade = "Pampulha"
elif mapa_selecionado == 55:
    coordenadas_iniciais = [-19.8779747,-43.9605378]
    localidade = "Maria Virgínia"
elif mapa_selecionado == 59 or mapa_selecionado == 60 or mapa_selecionado == 61 or mapa_selecionado == 62:
    coordenadas_iniciais = [-19.9174779, -43.8899357]
    localidade = "Taquaril"
elif mapa_selecionado == 63:
    coordenadas_iniciais = [-19.9085598, -43.893908]
    localidade = "Granja de Freitas"
elif mapa_selecionado == 64 or mapa_selecionado == 65 or mapa_selecionado == 66 or mapa_selecionado == 67:
    coordenadas_iniciais = [-19.9104093, -43.9038813]
    localidade = "Vera Cruz"
elif mapa_selecionado == 68:
    coordenadas_iniciais = [-19.8988885, -43.8976125]
    localidade = "Casa Branca"
elif mapa_selecionado == 69:
    coordenadas_iniciais = [-19.9123693, -43.9396475]
    localidade = "Floresta"
elif mapa_selecionado == 70:
    coordenadas_iniciais = [-19.9123693, -43.9396475]
    localidade = " Sagrada Familia "
elif mapa_selecionado == 73:
    coordenadas_iniciais = [-19.8879951, -43.9032698]
    localidade = "Nova Vista"
elif mapa_selecionado == 74:
    coordenadas_iniciais = [-19.8940462, -43.9105942]
    localidade = "Boa vista"
elif mapa_selecionado == 75 or mapa_selecionado == 76:
    coordenadas_iniciais = [-19.8993808, -43.9030014]
    localidade = "São Geraldo"
elif mapa_selecionado == 77:
    coordenadas_iniciais = [-19.8809719, -43.9325572]
    localidade = "União"
elif mapa_selecionado == 78:
    coordenadas_iniciais = [-19.8859333, -43.9205631]
    localidade = "Santa Inês"
elif mapa_selecionado == 79:
    coordenadas_iniciais = [-19.8685638, -43.9290117]
    localidade = "São Paulo"
elif mapa_selecionado == 80:
    coordenadas_iniciais = [-19.8715863, -43.9172112]
    localidade = "São Marcos"
elif mapa_selecionado == 81 or mapa_selecionado == 82:
    coordenadas_iniciais = [-19.8626487,-43.9149794]
    localidade = "Maria Goretti"
elif mapa_selecionado == 83:
    coordenadas_iniciais = [-19.8556552, -43.9269363]
    localidade = "São Gabriel"
elif mapa_selecionado == 84 or mapa_selecionado == 85:
    coordenadas_iniciais = [-19.8516162, -43.9153362]
    localidade = "Nazaré"
elif mapa_selecionado == 86:
    coordenadas_iniciais = [-19.8465458,-43.9127824]
    localidade = "Ouro minas"
elif mapa_selecionado == 87 or mapa_selecionado == 88:
    coordenadas_iniciais = [-19.8471814,-43.9283641]
    localidade = "Novo Aarão Reis"
elif mapa_selecionado == 89:
    coordenadas_iniciais = [-19.8290822, -43.9096156]
    localidade = "Ribeiro de Abreu"
elif mapa_selecionado == 90:
    coordenadas_iniciais =[-19.8401713, -43.9015157]
    localidade = "Paulo VI"
elif mapa_selecionado == 91:
    coordenadas_iniciais = [-19.8531743, -43.8951311]
    localidade = "Capitão Eduardo"
elif mapa_selecionado == 92:
    coordenadas_iniciais = [-19.8531743, -43.8951311]
    localidade = "Jardim Vitória"
else: 
    coordenadas_iniciais = [-19.912998, -43.940933]  # Belo Horizonte

st.write("-----")

st.subheader("Cartão Mapa de Território")

st.write(" Localidade : ****** ", localidade,"   ******" ,"  ________________  ", "   Território Nº :  " , mapa_selecionado)

# Buscar e exibir endereços associados ao mapa
enderecos = buscar_enderecos_por_mapa(mapa_selecionado)

# Barra lateral para selecionar o número do mapa e informações adicionais

if 0 < mapa_selecionado <= 93:
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
    st_data = st_folium(mapa_interativo, width=800, height=450)
    time.sleep(1.5)

    

# Exibe os endereços como links para o Google Maps e Waze
st.subheader("Endereços no Google Maps e Waze")

# Cria uma lista de dicionários para cada endereço, incluindo os links formatados
enderecos_dados = []
for endereco in enderecos:
    id_endereco, numero_mapa, numero_endereco, sexo, nome, latitude, longitude = endereco
    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    waze_link = f"https://www.waze.com/ul?ll={latitude},{longitude}&navigate=yes"
    enderecos_dados.append({
        "Número do Endereço": numero_endereco,
        "Sexo": sexo,
        "Endereço": nome,
        "Google Maps": f'<a href="{google_maps_link}" target="_blank">Google Maps</a>',
        "Waze": f'<a href="{waze_link}" target="_blank">Waze</a>'
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
