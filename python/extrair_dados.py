import sqlite3
import pandas as pd

# Caminho da base de dados
CAMINHO_BD = r"C:\Users\Vanessa Mello  Souza\Desktop\Projeto_Ecommerce\ecommerce_sales.db"


def obter_conexao():
    """Criar ligação à base de dados."""
    return sqlite3.connect(CAMINHO_BD)


def carregar_tabela(nome_tabela):
    """Carregar uma tabela da base de dados para um DataFrame."""
    conexao = obter_conexao()

    try:
        df = pd.read_sql_query(
            f'SELECT * FROM "{nome_tabela}"',
            conexao
        )
        return df
    finally:
        conexao.close()