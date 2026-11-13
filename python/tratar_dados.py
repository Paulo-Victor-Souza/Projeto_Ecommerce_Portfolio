import pandas as pd


def tratar_encomendas(df):
    """Preparar e tratar os dados das encomendas."""

    # Copiar os dados para preservar o DataFrame original
    df = df.copy()

    # Converter as colunas para formato de data
    colunas_data = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for coluna in colunas_data:
        df[coluna] = pd.to_datetime(
            df[coluna],
            errors="coerce"
        )

    # Calcular os dias de diferença entre entrega real e estimada
    df["dias_atraso"] = (
        df["order_delivered_customer_date"]
        - df["order_estimated_delivery_date"]
    ).dt.days

    # Identificar entregas atrasadas
    df["entrega_atrasada"] = pd.Series(
        pd.NA,
        index=df.index,
        dtype="boolean"
    )

    mask = df["order_delivered_customer_date"].notna()

    df.loc[mask, "entrega_atrasada"] = (
            df.loc[mask, "order_delivered_customer_date"]
            >
            df.loc[mask, "order_estimated_delivery_date"]
    )

    return df

def tratar_produtos(df):
    df = df.copy()

    print("\nVALORES EM FALTA NOS PRODUTOS")
    print(df.isnull().sum())

    df["product_category_name"] = (
        df["product_category_name"]
        .str.strip()
        .fillna("sem_categoria")
    )

    colunas_texto = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty"
    ]

    for coluna in colunas_texto:
        df[coluna] = pd.to_numeric(
            df[coluna], errors="coerce"
        )

    return df
def tratar_clientes(df):
    """Preparar e tratar os dados dos clientes."""

    df = df.copy()

    # Verificar valores em falta
    print("\nVALORES EM FALTA NOS CLIENTES")
    print(df.isnull().sum())

    # Remover espaços desnecessários
    colunas_texto = [
        "customer_city",
        "customer_state"
    ]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    # Uniformizar nomes das cidades
    df["customer_city"] = (
        df["customer_city"].str.title()
    )

    # Uniformizar códigos dos estados
    df["customer_state"] = (
        df["customer_state"].str.upper()
    )

    return df
def tratar_vendas(df):
    """Preparar e tratar os dados dos itens das encomendas."""

    df = df.copy()

    print("\nVALORES EM FALTA NAS VENDAS")
    print(df.isnull().sum())

    # Converter a data de envio para formato datetime
    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"],
        errors="coerce"
    )

    # Garantir que os valores são numéricos
    colunas_valor = ["price", "freight_value"]

    for coluna in colunas_valor:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    # Calcular o valor total do item com portes
    df["valor_total_item"] = (
        df["price"] + df["freight_value"]
    )

    return df
def tratar_pagamentos(df):
    df = df.copy()

    print("\nVALORES EM FALTA NOS PAGAMENTOS")
    print(df.isnull().sum())

    df["payment_type"] = df["payment_type"].str.strip().str.lower()

    df["payment_value"] = pd.to_numeric(
        df["payment_value"], errors="coerce"
    )

    return df
def tratar_avaliacoes(df):
    df = df.copy()

    print("\nVALORES EM FALTA NAS AVALIAÇÕES")
    print(df.isnull().sum())

    df["review_score"] = pd.to_numeric(
        df["review_score"], errors="coerce"
    )

    df["review_comment_title"] = (
        df["review_comment_title"].fillna("")
    )

    df["review_comment_message"] = (
        df["review_comment_message"].fillna("")
    )

    return df
def tratar_vendedores(df):
    df = df.copy()

    print("\nVALORES EM FALTA NOS VENDEDORES")
    print(df.isnull().sum())

    df["seller_city"] = df["seller_city"].str.strip().str.title()
    df["seller_state"] = df["seller_state"].str.strip().str.upper()

    return df

def tratar_geolocalizacao(df):
    df = df.copy()

    df["geolocation_city"] = (
        df["geolocation_city"].str.strip().str.title()
    )

    df["geolocation_state"] = (
        df["geolocation_state"].str.strip().str.upper()
    )

    df["geolocation_lat"] = pd.to_numeric(
        df["geolocation_lat"], errors="coerce"
    )

    df["geolocation_lng"] = pd.to_numeric(
        df["geolocation_lng"], errors="coerce"
    )

    # Remover apenas duplicados exatos
    df = df.drop_duplicates()

    return df

def resumir_geolocalizacao(df):
    df = df.copy()

    df_resumido = (
        df.groupby("geolocation_zip_code_prefix", as_index=False)
        .agg({
            "geolocation_lat": "mean",
            "geolocation_lng": "mean",
            "geolocation_city": "first",
            "geolocation_state": "first"
        })
    )

    return df_resumido