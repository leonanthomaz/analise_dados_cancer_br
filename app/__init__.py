import os
from flask import Flask, render_template
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Configurando Kaggle API
api = KaggleApi()
api.authenticate()

# Baixando o dataset do Kaggle
dataset_name = 'joaopedromedeiros/cancer-data-brazil'
download_path = 'data/' 
api.dataset_download_files(dataset_name, path=download_path, unzip=True)

# Lendo o dataset
csv_file = os.path.join(download_path, 'cancer_data_eng.csv')
df = pd.read_csv(csv_file, encoding='ISO-8859-1')
pd.set_option('display.max_columns', None)

# Configurando Flask
app = Flask(__name__, static_folder="templates")

# Página inicial com cards para análises
@app.route("/")
def index():
    return render_template("index.html")

# Rota: Diagnósticos por gênero
@app.route("/gender_analysis")
def gender_analysis():
    # Gráfico de barras: Diagnósticos por gênero
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    fig = px.bar(gender_counts, x='Gender', y='Count', title="Diagnósticos por Gênero", labels={'Gender': 'Gênero', 'Count': 'Frequência'})
    fig.update_layout(template="plotly_white")
    graph_html = pio.to_html(fig, full_html=False)

    return render_template("analysis.html", title="Análise por Gênero", graph=graph_html)

# Rota: Distribuição de idades
@app.route("/age_distribution")
def age_distribution():
    fig = px.histogram(
        df,
        x='Age',
        title="Distribuição de Idades",
        labels={'Age': 'Idade', 'count': 'Frequência'},
        # nbins=20  # Número de bins ajustado
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Idade",
        yaxis_title="Frequência",
        xaxis=dict(range=[0, 120]) 
    )
    graph_html = pio.to_html(fig, full_html=False)

    return render_template("analysis.html", title="Distribuição de Idades", graph=graph_html)

# Rota: Frequência de doenças *** Em manutenção
@app.route("/disease_frequency")
def disease_frequency():
    # Gráfico de pizza: Frequência de tipos de doença
    disease_counts = df['Description.of.Disease'].value_counts().reset_index()
    disease_counts.columns = ['Disease', 'Count']

    # Agrupar doenças menos frequentes em "Outras"
    threshold = 50
    disease_counts['Disease'] = disease_counts.apply(
        lambda row: row['Disease'] if row['Count'] >= threshold else 'Outras', axis=1
    )
    grouped_disease_counts = disease_counts.groupby('Disease')['Count'].sum().reset_index()

    fig = px.pie(
        grouped_disease_counts,
        names='Disease',
        values='Count',
        title="Frequência de Tipos de Doença"
    )
    fig.update_layout(template="plotly_white", showlegend=True)
    graph_html = pio.to_html(fig, full_html=False)

    return render_template("analysis.html", title="Frequência de Tipos de Doença", graph=graph_html)

# Rota: Doenças mais comuns por faixa etária
@app.route("/diseases_by_age")
def diseases_by_age():
    # Verificando se as colunas necessárias existem
    if 'Age' not in df.columns or 'Description.of.Disease' not in df.columns:
        return "Erro: A coluna 'Age' (idade) ou 'Description.of.Disease' (Tipo de Cancer) não foi encontrada no dataset.", 400

    # Definindo faixas etárias (ajuste os intervalos conforme necessário)
    bins = [0, 18, 30, 40, 50, 60, 70, 100]
    labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61-70', '71+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # Agrupando por faixa etária e doença
    age_disease_counts = df.groupby(['Age Group', 'Description.of.Disease']).size().reset_index(name='Count')

    # Verificando se o agrupamento deu certo
    if age_disease_counts.empty:
        return "Erro: Não foi possível agrupar os dados por faixa etária e doença.", 400

    # Criando o gráfico de barras para doenças mais comuns por faixa etária
    fig = px.bar(age_disease_counts, x='Age Group', y='Count', color='Description.of.Disease', barmode='stack',
                 title="Doenças Mais Comuns por Faixa Etária", labels={'Age Group': 'Faixa Etária', 'Count': 'Número de Casos', 'Description.of.Disease' : 'Tipo de Cancer'})
    fig.update_layout(template="plotly_white")
    graph_html = pio.to_html(fig, full_html=False)

    return render_template("analysis.html", title="Doenças Mais Comuns por Faixa Etária", graph=graph_html)

# Rota: Análise de câncer em crianças e adolescentes
@app.route("/youth_cancer_analysis")
def youth_cancer_analysis():
    # Verificando se as colunas necessárias existem
    if 'Age' not in df.columns or 'Date.of.Diagnostic' not in df.columns or 'Description.of.Disease' not in df.columns:
        return "Erro: As colunas necessárias não foram encontradas no dataset.", 400

    # Filtrando para crianças e adolescentes (0-18 anos)
    youth_data = df[df['Age'] <= 18]

    # Verificando se há dados após o filtro
    if youth_data.empty:
        return "Erro: Nenhum dado encontrado para crianças e adolescentes.", 400

    # Convertendo a coluna 'Date.of.Diagnostic' para datetime, se necessário
    try:
        youth_data['Date.of.Diagnostic'] = pd.to_datetime(youth_data['Date.of.Diagnostic'])
    except Exception as e:
        return f"Erro ao converter a coluna 'Date.of.Diagnostic' para datetime: {e}", 400

    # Adicionando a coluna de período com base no ano do diagnóstico
    youth_data['Período'] = pd.cut(
        youth_data['Date.of.Diagnostic'].dt.year,
        bins=[1999, 2010, 2019],
        labels=['2000-2010', '2010-2019'],
        right=False
    )

    # Verificando se há dados após a divisão em períodos
    if youth_data['Período'].isnull().all():
        return "Erro: Nenhum dado encontrado nos períodos especificados (2000-2019).", 400

    # Contando a frequência de tipos de câncer por período
    cancer_counts = (
        youth_data.groupby(['Período', 'Description.of.Disease'])
        .size()
        .reset_index(name='Frequência')
    )

    disease_counts = cancer_counts.groupby('Description.of.Disease')['Frequência'].sum() 
    valid_diseases = disease_counts[disease_counts > 100].index 
    filtered_cancer_counts = cancer_counts[cancer_counts['Description.of.Disease'].isin(valid_diseases)]
    
    # Criando o gráfico de barras para comparar os períodos
    fig = px.bar(
        filtered_cancer_counts,
        x='Description.of.Disease',
        y='Frequência',
        color='Período',
        barmode='group',
        title="Cânceres Predominantes em Crianças e Adolescentes (2000-2019)",
        labels={'Description.of.Disease': 'Tipo de Câncer', 'Frequência': 'Número de Casos'}
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Tipo de Câncer",
        yaxis_title="Número de Casos",
        xaxis={'categoryorder': 'total descending'}  # Ordenar os tipos de câncer pela frequência total
    )

    # Convertendo o gráfico para HTML
    graph_html = pio.to_html(fig, full_html=False)

    return render_template(
        "analysis.html",
        title="Câncer em Crianças e Adolescentes",
        graph=graph_html
    )


# Função para rodar o app
def create_app():
    app.run(debug=True)

