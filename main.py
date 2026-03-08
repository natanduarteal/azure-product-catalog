import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymysql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()
BlobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
BlobContainerName = os.getenv("BLOB_CONTAINER_NAME")
BlobAccountName = os.getenv("BLOB_ACCOUNT_NAME")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")    
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

st.title("Cadastro de produtos")

# Formulário de cadastro de produtos
product_name = st.text_input("Nome do produto")
product_price = st.number_input("Preço do produto", min_value=0.0, format="%.2f")
product_description = st.text_area("Descrição do produto")
product_image = st.file_uploader("Imagem do produto", type=["jpg", "jpeg", "png"])

#Save image on Azure Blob Storage
def upload_image_to_blob(image_file):
    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
    container_client = blob_service_client.get_container_client(BlobContainerName)
    blob_name = f"{uuid.uuid4()}_{image_file.name}"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(image_file, overwrite=True)
    image_url = f"https://{BlobAccountName}.blob.core.windows.net/{BlobContainerName}/{blob_name}"
    return image_url

def insert_product_to_db(name, price, description, image_url):
    try:
        image_url=upload_image_to_blob(product_image)
        conn=pymysql.connect(host=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor=conn.cursor()
        insert_sql = "INSERT INTO Produtos (nome, preco, descricao, image_url) VALUES (%s, %s, %s, %s)"
        print(insert_sql)
        cursor.execute(insert_sql, (name, price, description, image_url))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao cadastrar produto: {e}")
        return False

if st.button("Cadastrar produto"):
    insert_product_to_db(name=product_name, price=product_price, description=product_description, image_url=upload_image_to_blob(product_image))
    return_message = "Produto cadastrado com sucesso!"

st.header("Produtos cadastrados")

if st.button("Listar produtos"):
    try:
        conn = pymysql.connect(host=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT nome, preco, descricao, image_url FROM Produtos")
        products = cursor.fetchall()
        conn.close()

        for product in products:
            st.subheader(product[0])
            st.write(f"Preço: R$ {product[1]:.2f}")
            st.write(f"Descrição: {product[2]}")
            st.image(product[3], width=200)
        return_message = "Produtos listados com sucesso!"
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return_message = "Erro ao listar produtos."