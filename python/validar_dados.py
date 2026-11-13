
import pandas as pd
import os

PASTA_RELATORIOS = (
    r"C:\Users\Vanessa Mello  Souza\Desktop"
    r"\Projeto_Ecommerce\relatorios"
)

ficheiros = [
    "encomendas_tratadas.csv",
    "produtos_tratados.csv",
    "clientes_tratados.csv",
    "vendas_tratadas.csv",
    "pagamentos_tratados.csv",
    "avaliacoes_tratadas.csv",
    "vendedores_tratados.csv",
    "geolocalizacao_tratada.csv"
]

print("VALIDAÇÃO DOS FICHEIROS ETL")

for ficheiro in ficheiros:
    caminho = os.path.join(PASTA_RELATORIOS, ficheiro)

    if os.path.exists(caminho):
        df = pd.read_csv(caminho)

        print("\nFicheiro:", ficheiro)
        print("Registos:", len(df))
        print("Colunas:", len(df.columns))
        print("Duplicados:", df.duplicated().sum())
        print("Valores em falta:", df.isnull().sum().sum())

    else:
        print("\nFicheiro não encontrado:", ficheiro)


# Análise detalhada das avaliações

print("\n" + "=" * 40)
print("ANÁLISE DETALHADA DAS AVALIAÇÕES")
print("=" * 40)

df_avaliacoes = pd.read_csv(
    os.path.join(PASTA_RELATORIOS, "avaliacoes_tratadas.csv"),
    keep_default_na=False
)

print("\nValores em falta por coluna:")
print(df_avaliacoes.isnull().sum())

print("\nTotal de valores em falta:")
print(df_avaliacoes.isnull().sum().sum())

print("\nANÁLISE DETALHADA DOS PRODUTOS")

df_produtos = pd.read_csv(
    os.path.join(PASTA_RELATORIOS, "produtos_tratados.csv")
)

print("\nValores em falta por coluna:")
print(df_produtos.isnull().sum())

print("\nProdutos sem categoria:")
print(
    df_produtos[
        df_produtos["product_category_name"] == "sem_categoria"
    ].shape[0]
)

print("\nANÁLISE DETALHADA DAS ENCOMENDAS")

df_encomendas = pd.read_csv(
    os.path.join(PASTA_RELATORIOS, "encomendas_tratadas.csv")
)

print("\nValores em falta por coluna:")
print(df_encomendas.isnull().sum())

print("\nValores em falta por estado da encomenda:")

print(
    df_encomendas.groupby("order_status")[
        "order_delivered_customer_date"
    ].apply(lambda x: x.isnull().sum())
)
print("\nENCOMENDAS ENTREGUES SEM DATA DE ENTREGA")

print(
    df_encomendas[
        (df_encomendas["order_status"] == "delivered") &
        (df_encomendas["order_delivered_customer_date"].isnull())
    ][
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_carrier_date",
            "order_estimated_delivery_date"
        ]
    ]
)
print("\nANÁLISE DA GEOLOCALIZAÇÃO")

df_geo = pd.read_csv(
    os.path.join(
        PASTA_RELATORIOS,
        "geolocalizacao_tratada.csv"
    )
)

print("\nDuplicados em todas as colunas:")
print(df_geo.duplicated().sum())

print("\nDuplicados por código postal:")
print(
    df_geo.duplicated(
        subset=["geolocation_zip_code_prefix"]
    ).sum()
)

print("\nCódigos postais distintos:")
print(
    df_geo["geolocation_zip_code_prefix"].nunique()
)

print("\nVALIDAÇÃO DA GEOLOCALIZAÇÃO RESUMIDA")

df_geo_resumida = pd.read_csv(
    os.path.join(
        PASTA_RELATORIOS,
        "geolocalizacao_resumida.csv"
    )
)

print("Total de registos:", len(df_geo_resumida))

print(
    "Códigos postais duplicados:",
    df_geo_resumida.duplicated(
        subset=["geolocation_zip_code_prefix"]
    ).sum()
)

print(
    "Códigos postais distintos:",
    df_geo_resumida["geolocation_zip_code_prefix"].nunique()
)

print(
    "Valores em falta:",
    df_geo_resumida.isnull().sum().sum()
)