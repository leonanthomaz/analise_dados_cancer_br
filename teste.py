from json import detect_encoding
import pandas as pd

def load_and_inspect_data(file_path):
    """Carrega e inspeciona o dataset."""
    try:
        # Detecta a codificação do arquivo
        encoding = detect_encoding(file_path)
        print(f"Codificação detectada: {encoding}")

        # Lendo o arquivo CSV com a codificação detectada
        df = pd.read_csv(file_path, encoding=encoding)
        pd.set_option('display.max_columns', None)  # Mostra todas as colunas

        # Exibindo as primeiras linhas
        print("Primeiras linhas do dataset:")
        print(df.head())

        # Exibindo informações gerais do dataset
        print("\nInformações do dataset:")
        print(df.info())

        # Exibindo estatísticas descritivas
        print("\nEstatísticas descritivas:")
        print(df.describe(include="all"))

        return df
    
    except Exception as e:
        print(f"Erro ao carregar o dataset: {e}")
        return None

if __name__ == "__main__":
    file_path = 'cancer_data_eng.csv'
    df = load_and_inspect_data(file_path)
