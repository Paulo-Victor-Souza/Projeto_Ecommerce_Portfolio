
import sqlite3
import pandas as pd

# Caminho da base de dados
caminho_bd = r"C:\Users\Vanessa Mello  Souza\Desktop\Projeto_Ecommerce\ecommerce_sales.db"

# Ligar à base de dados
conexao = sqlite3.connect(caminho_bd)

# Importar os dados das encomendas para um DataFrame
df_encomendas = pd.read_sql_query(
    "SELECT * FROM olist_orders_dataset",
    conexao
)

# Analisar os estados das encomendas
resultado = (
    df_encomendas["order_status"]
    .value_counts()
    .reset_index()
)

resultado.columns = ["Estado da encomenda", "Quantidade"]

# Calcular percentagens
resultado["Percentagem"] = (
    resultado["Quantidade"] / len(df_encomendas) * 100
).round(2)

print("ANÁLISE DOS ESTADOS DAS ENCOMENDAS")
print(resultado.to_string(index=False))

print("\nTotal de encomendas:", len(df_encomendas))


# ANÁLISE PYTHON 2: Vendas por categoria de produto

consulta = """
SELECT
    p.product_category_name AS categoria,
    COUNT(*) AS quantidade_artigos,
    ROUND(SUM(i.price), 2) AS valor_total_artigos
FROM olist_order_items_dataset AS i
INNER JOIN olist_products_dataset AS p
    ON i.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY valor_total_artigos DESC
LIMIT 10;
"""

df_categorias = pd.read_sql_query(consulta, conexao)

print("\nTOP 10 CATEGORIAS POR VALOR DE ARTIGOS")
print(df_categorias.to_string(index=False))


# ANÁLISE PYTHON 3: Métodos de pagamento

consulta_pagamentos = """
SELECT
    payment_type AS metodo_pagamento,
    COUNT(*) AS total_registos,
    ROUND(SUM(payment_value), 2) AS valor_total
FROM olist_order_payments_dataset
GROUP BY payment_type
ORDER BY valor_total DESC;
"""

df_pagamentos = pd.read_sql_query(
    consulta_pagamentos,
    conexao
)

print("\nANÁLISE DOS MÉTODOS DE PAGAMENTO")
print(df_pagamentos.to_string(index=False))

# ANÁLISE PYTHON 4: Verificar valores em falta nas encomendas

df_encomendas = pd.read_sql_query(
    "SELECT * FROM olist_orders_dataset",
    conexao
)

valores_em_falta = df_encomendas.isnull().sum()

print("\nVALORES EM FALTA NA TABELA DE ENCOMENDAS")
print(valores_em_falta[valores_em_falta > 0])

# ANÁLISE PYTHON 5: Valores em falta por estado da encomenda

consulta = """
SELECT
    order_status,
    COUNT(*) AS total_encomendas,
    SUM(
        CASE
            WHEN order_delivered_customer_date IS NULL
            THEN 1 ELSE 0
        END
    ) AS sem_data_entrega
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY sem_data_entrega DESC;
"""

df_faltas = pd.read_sql_query(consulta, conexao)

print("\nVALORES EM FALTA POR ESTADO DA ENCOMENDA")
print(df_faltas.to_string(index=False))

# PREPARAÇÃO 1: Carregar dados das encomendas

consulta = """
SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date
FROM olist_orders_dataset;
"""

df_encomendas = pd.read_sql_query(consulta, conexao)

print("\nDADOS DAS ENCOMENDAS")
print(df_encomendas.head())

print("\nTIPOS DE DADOS")
print(df_encomendas.dtypes)

print("\nVALORES EM FALTA")
print(df_encomendas.isnull().sum())

# PREPARAÇÃO 2: Converter colunas para formato de data

colunas_data = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for coluna in colunas_data:
    df_encomendas[coluna] = pd.to_datetime(
        df_encomendas[coluna],
        errors="coerce"
    )

print("\nTIPOS DE DADOS APÓS CONVERSÃO")
print(df_encomendas.dtypes)

print("\nEXEMPLO DAS DATAS")
print(df_encomendas[colunas_data].head())

# PREPARAÇÃO 3: Calcular dias de atraso na entrega

df_encomendas["dias_atraso"] = (
    df_encomendas["order_delivered_customer_date"]
    - df_encomendas["order_estimated_delivery_date"]
).dt.days

# Classificar corretamente as entregas
df_encomendas["entrega_atrasada"] = (
    df_encomendas["order_delivered_customer_date"]
    >
    df_encomendas["order_estimated_delivery_date"]
)

print("\nANÁLISE DOS ATRASOS")
print(
    df_encomendas[
        [
            "order_status",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "dias_atraso",
            "entrega_atrasada"
        ]
    ].head(10).to_string(index=False)
)

print("\nRESUMO DOS DIAS DE ATRASO")
print(df_encomendas["dias_atraso"].describe())

# PREPARAÇÃO 4: Resumo do desempenho das entregas

df_entregas = df_encomendas[
    df_encomendas["order_status"] == "delivered"
].copy()

total_entregues = len(df_entregas)

entregas_atrasadas = (
    df_entregas["dias_atraso"] > 0
).sum()

entregas_no_prazo = (
    df_entregas["dias_atraso"] <= 0
).sum()

percentagem_atrasadas = (
    entregas_atrasadas / total_entregues
) * 100

percentagem_no_prazo = (
    entregas_no_prazo / total_entregues
) * 100

print("\nDESEMPENHO DAS ENTREGAS")
print("Total de encomendas entregues:", total_entregues)
print("Entregas atrasadas:", entregas_atrasadas)
print("Entregas no prazo:", entregas_no_prazo)
print(f"Percentagem de atrasos: {percentagem_atrasadas:.2f}%")
print(f"Percentagem dentro do prazo: {percentagem_no_prazo:.2f}%")

# VALIDAÇÃO: Comparar datas e horas completas

entregas_validas = df_entregas.dropna(
    subset=[
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
).copy()

entregas_validas["atraso_data_hora"] = (
    entregas_validas["order_delivered_customer_date"]
    >
    entregas_validas["order_estimated_delivery_date"]
)

total_atrasadas_hora = entregas_validas["atraso_data_hora"].sum()

print("\nVALIDAÇÃO DO CÁLCULO DOS ATRASOS")
print("Entregas com datas disponíveis:", len(entregas_validas))
print("Atrasadas considerando data e hora:", total_atrasadas_hora)

# PREPARAÇÃO 5: Exportar dados tratados para CSV

import os

# Caminho da pasta principal do projeto
pasta_projeto = r"C:\Users\Vanessa Mello  Souza\Desktop\Projeto_Ecommerce"

# Criar a pasta relatorios, caso ainda não exista
pasta_relatorios = os.path.join(pasta_projeto, "relatorios")
os.makedirs(pasta_relatorios, exist_ok=True)

# Caminho do ficheiro CSV
caminho_csv = os.path.join(
    pasta_relatorios,
    "encomendas_tratadas.csv"
)

# Exportar os dados
df_encomendas.to_csv(
    caminho_csv,
    index=False,
    encoding="utf-8-sig"
)

print("\nEXPORTAÇÃO CONCLUÍDA!")
print("Ficheiro guardado em:", caminho_csv)
print("Total de registos exportados:", len(df_encomendas))
# Fechar ligação
conexao.close()
