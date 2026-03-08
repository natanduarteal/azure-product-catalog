# azure-product-catalog

🛒 Sistema de Cadastro de Produtos com Azure Cloud
Este projeto é uma aplicação web desenvolvida para o gerenciamento de catálogos de produtos, integrando serviços de nuvem da Microsoft Azure para armazenamento de arquivos e persistência de dados.

🚀 Funcionalidades
Cadastro de Produtos: Interface intuitiva para inserção de nome, preço e descrição.

Upload de Imagens: Integração com Azure Blob Storage para armazenamento de fotos dos produtos.

Listagem Dinâmica: Exibição dos produtos cadastrados consumindo dados em tempo real do banco de dados.

🛠️ Arquitetura do Projeto
A aplicação foi construída utilizando:

Frontend: Streamlit para uma interface rápida e responsiva.

Armazenamento de Imagens: Azure Blob Storage para hospedar os arquivos de mídia de forma escalável.

Banco de Dados: Azure SQL Database para armazenar os metadados dos produtos.

Conectividade: Bibliotecas pyodbc (para SQL Server) e azure-storage-blob.
