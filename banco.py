import streamlit as st
import pandas as pd
import folium
import sqlite3

st.set_page_config(page_title="Ls Maps", page_icon="Images/ls2.png", layout="wide")


# Interface do usuário
st.logo(image="images/libras.png", icon_image="images/libras.png")

# Defina a senha correta
senha_correta = "mapas"

# Função para verificar a senha
def verificar_senha():
    # Solicitar a senha antes de carregar a página
    senha_fornecida = st.text_input("Digite a senha:", type="password")
    if senha_fornecida == senha_correta:
        return True
    elif senha_fornecida:
        st.error("Senha incorreta. Tente novamente.")
        return False
    return False

# Verifica se a senha está correta antes de carregar a página
if verificar_senha():
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

    # Função para adicionar endereço
    def adicionar_endereco(numero_mapa, numero_endereco, sexo, nome, latitude, longitude):
        c.execute("INSERT INTO enderecos (numero_mapa, numero_endereco, sexo, nome, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)", 
                  (numero_mapa, numero_endereco, sexo, nome, (latitude), (longitude)))
        conn.commit()

    # Função para deletar endereço
    def deletar_endereco(id):
        c.execute("DELETE FROM enderecos WHERE id = ?", (id,))
        conn.commit()

    # Função para atualizar endereço
    def atualizar_endereco(id, numero_mapa, numero_endereco, sexo, nome, latitude, longitude):
        c.execute("UPDATE enderecos SET numero_mapa = ?, numero_endereco = ?, sexo = ?, nome = ?, latitude = ?, longitude = ? WHERE id = ?", 
                  (numero_mapa, numero_endereco, sexo, nome, (latitude), (longitude), id))
        conn.commit()

    # Função para buscar endereços por número do mapa
    def buscar_enderecos_por_mapa(numero_mapa):
        c.execute("SELECT * FROM enderecos WHERE numero_mapa = ?", (numero_mapa,))
        return c.fetchall()

    # Seleção do número do mapa
    numero_mapa = st.number_input("Selecione o número do mapa", min_value=1, step=1)

    # Buscar e exibir endereços associados ao mapa
    enderecos = buscar_enderecos_por_mapa(numero_mapa)

    if enderecos:
        st.subheader(f"Endereços associados ao Mapa {numero_mapa}")
        for endereco in enderecos:
            id_endereco, numero_mapa, numero_endereco, sexo, nome, latitude, longitude = endereco
            st.markdown(f"[{nome}](https://www.google.com/maps/search/?api=1&query={latitude},{longitude})")
    else:
        st.write(f"Não há endereços cadastrados para o Mapa {numero_mapa}")

    # Adicionar novo endereço
    st.subheader("Adicionar novo endereço")
    with st.form(key="adicionar_endereco"):
        numero_endereco = st.text_input("Numero do endereço")
        sexo = st.text_input("Sexo (H/M/C)")
        nome = st.text_input("Nome do endereço")
        latitude = st.number_input("Latitude", format="%.8f")
        longitude = st.number_input("Longitude", format="%.8f")
        submit_button = st.form_submit_button(label="Adicionar Endereço")

        if submit_button:
            adicionar_endereco(numero_mapa, numero_endereco, sexo, nome, latitude, longitude)
            st.success("Endereço adicionado com sucesso!")

    # Deletar endereço
    st.subheader("Deletar endereço")
    id_deletar = st.number_input("ID do endereço a ser deletado", min_value=1, step=1)
    if st.button("Deletar Endereço"):
        deletar_endereco(id_deletar)
        st.success("Endereço deletado com sucesso!")

    # Atualizar endereço
    st.subheader("Atualizar endereço")
    id_atualizar = st.number_input("ID do endereço a ser atualizado", min_value=1, step=1)
    with st.form(key="atualizar_endereco"):
        numero_endereco = st.text_input("Numero do endereço", value="")
        sexo = st.text_input("Sexo (H/M/C)", value="")
        nome = st.text_input("Nome do endereço", value="")
        latitude = st.number_input("Latitude", format="%.8f")
        longitude = st.number_input("Longitude", format="%.8f")
        submit_button = st.form_submit_button(label="Atualizar Endereço")

        if submit_button:
            atualizar_endereco(id_atualizar, numero_mapa, numero_endereco, sexo, nome, latitude, longitude)
            st.success("Endereço atualizado com sucesso!")

    # Fechar a conexão com o banco de dados
    conn.close()

