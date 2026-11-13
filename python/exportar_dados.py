import os


# Caminho da pasta de relatórios
PASTA_RELATORIOS = (
    r"C:\Users\Vanessa Mello  Souza\Desktop"
    r"\Projeto_Ecommerce\relatorios"
)


def exportar_csv(df, nome_ficheiro):
    """Exportar um DataFrame para um ficheiro CSV."""

    os.makedirs(PASTA_RELATORIOS, exist_ok=True)

    caminho = os.path.join(
        PASTA_RELATORIOS,
        nome_ficheiro
    )

    df.to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Ficheiro exportado: {caminho}")
    print(f"Total de registos: {len(df)}")