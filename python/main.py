from extrair_dados import carregar_tabela
from tratar_dados import (
    tratar_encomendas,
    tratar_produtos,
    tratar_clientes,
    tratar_vendas,
    tratar_pagamentos,
    tratar_avaliacoes,
    tratar_vendedores,
    tratar_geolocalizacao,
    resumir_geolocalizacao
)
from exportar_dados import exportar_csv


def main():

    print("A INICIAR PROCESSO ETL")

    # 1. Extrair dados da base de dados
    print("\n1. A carregar encomendas...")

    df_encomendas = carregar_tabela(
        "olist_orders_dataset"
    )

    print("Encomendas carregadas:", len(df_encomendas))

    # 2. Tratar os dados
    print("\n2. A tratar encomendas...")

    df_encomendas = tratar_encomendas(df_encomendas)

    print("Tratamento concluído!")

    # 3. Exportar os dados
    print("\n3. A exportar ficheiro...")

    exportar_csv(
        df_encomendas,
        "encomendas_tratadas.csv"
    )
    # 4. Extrair dados dos produtos
    print("\n4. A carregar produtos...")

    df_produtos = carregar_tabela(
        "olist_products_dataset"
    )

    print("Produtos carregados:", len(df_produtos))

    # 5. Tratar dados dos produtos
    print("\n5. A tratar produtos...")

    df_produtos = tratar_produtos(df_produtos)

    print("Tratamento dos produtos concluído!")

    # 6. Exportar produtos
    print("\n6. A exportar produtos...")

    exportar_csv(
        df_produtos,
        "produtos_tratados.csv"
    )
    # 7. Extrair dados dos clientes
    print("\n7. A carregar clientes...")

    df_clientes = carregar_tabela(
        "olist_customers_dataset"
    )

    print("Clientes carregados:", len(df_clientes))

    # 8. Tratar dados dos clientes
    print("\n8. A tratar clientes...")

    df_clientes = tratar_clientes(df_clientes)

    print("Tratamento dos clientes concluído!")

    # 9. Exportar clientes
    print("\n9. A exportar clientes...")

    exportar_csv(
        df_clientes,
        "clientes_tratados.csv"
    )
    # 10. Extrair dados das vendas
    print("\n10. A carregar vendas...")

    df_vendas = carregar_tabela(
        "olist_order_items_dataset"
    )

    print("Registos de vendas carregados:", len(df_vendas))

    # 11. Tratar dados das vendas
    print("\n11. A tratar vendas...")

    df_vendas = tratar_vendas(df_vendas)

    print("Tratamento das vendas concluído!")

    # 12. Exportar vendas
    print("\n12. A exportar vendas...")

    exportar_csv(
        df_vendas,
        "vendas_tratadas.csv"
    )
    print("\n13. A carregar pagamentos...")
    df_pagamentos = carregar_tabela("olist_order_payments_dataset")
    print("Registos de pagamentos carregados:", len(df_pagamentos))

    print("\n14. A tratar pagamentos...")
    df_pagamentos = tratar_pagamentos(df_pagamentos)

    print("\n15. A exportar pagamentos...")
    exportar_csv(df_pagamentos, "pagamentos_tratados.csv")

    print("\n16. A carregar avaliações...")
    df_avaliacoes = carregar_tabela("olist_order_reviews_dataset")
    print("Registos de avaliações carregados:", len(df_avaliacoes))

    print("\n17. A tratar avaliações...")
    df_avaliacoes = tratar_avaliacoes(df_avaliacoes)

    print("\n18. A exportar avaliações...")
    exportar_csv(df_avaliacoes, "avaliacoes_tratadas.csv")
    print("\n19. A carregar vendedores...")
    df_vendedores = carregar_tabela("olist_sellers_dataset")
    print("Registos de vendedores carregados:", len(df_vendedores))

    print("\n20. A tratar vendedores...")
    df_vendedores = tratar_vendedores(df_vendedores)

    print("\n21. A exportar vendedores...")
    exportar_csv(df_vendedores, "vendedores_tratados.csv")
    print("\n22. A carregar geolocalização...")
    df_geolocalizacao = carregar_tabela("olist_geolocation_dataset")
    print("Registos de geolocalização carregados:", len(df_geolocalizacao))

    print("\n22. A carregar geolocalização...")
    df_geolocalizacao = carregar_tabela("olist_geolocation_dataset")
    print("Registos de geolocalização carregados:", len(df_geolocalizacao))

    print("\n23. A tratar geolocalização...")
    df_geolocalizacao = tratar_geolocalizacao(df_geolocalizacao)

    print("\n24. A exportar geolocalização...")
    exportar_csv(df_geolocalizacao, "geolocalizacao_tratada.csv")

    print("\n25. A resumir geolocalização...")
    df_geolocalizacao_resumida = resumir_geolocalizacao(
        df_geolocalizacao
    )

    print("\n26. A exportar geolocalização resumida...")
    exportar_csv(
        df_geolocalizacao_resumida,
        "geolocalizacao_resumida.csv"
    )
    print("\nPROCESSO ETL CONCLUÍDO COM SUCESSO!")


if __name__ == "__main__":
    main()