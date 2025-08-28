## Análise de Dados de Câncer no Brasil (2000-2019)

Este projeto realiza uma análise exploratória de dados de câncer no Brasil, abrangendo o período de 2000 a 2019. Os dados foram obtidos do Kaggle ([https://www.kaggle.com/datasets/joaopedromedeiros/cancer-data-brazil](https://www.kaggle.com/datasets/joaopedromedeiros/cancer-data-brazil)) e compreendem informações de pacientes de centros de câncer em todo o país.

### Objetivo

O objetivo deste projeto é fornecer insights sobre os padrões de câncer no Brasil, incluindo a distribuição de diagnósticos por gênero, faixa etária e tipo de câncer, com foco em crianças e adolescentes.

### Metodologia

1.  **Coleta de Dados:** O dataset "cancer-data-brazil" foi baixado do Kaggle e descompactado.
2.  **Pré-processamento:** Os dados foram lidos e processados utilizando a biblioteca Pandas.
3.  **Análise Exploratória:** Foram realizadas análises descritivas para identificar padrões e tendências nos dados.
4.  **Visualização:** Os resultados foram visualizados através de gráficos interativos gerados com a biblioteca Plotly.
5.  **Aplicação Flask:** Uma aplicação web Flask foi desenvolvida para apresentar os resultados de forma interativa.

### Tecnologias

*   **Python:** Linguagem de programação utilizada para o desenvolvimento do projeto.
*   **Bibliotecas:**
    *   **Pandas:** Para manipulação e análise de dados.
    *   **Plotly:** Para criação de gráficos interativos.
    *   **Flask:** Para desenvolvimento da aplicação web.
    *   **Kaggle:** Para download do dataset.
*   **HTML/CSS:** Para estruturação e estilização das páginas web.
*   **Bootstrap:** Para estilização responsiva da interface web.

### Estrutura do Projeto

```
analise_dados_cancer_br:
│   .gitignore
│   LICENSE
│   README.md
│   requirements.txt
│   run.py
│   teste.py
│   
└───app
    │   __init__.py
    │   
    └───templates
           analysis.html
           index.html
    
```

### Como Executar

1.  **Clone o repositório:** `git clone https://github.com/leonanthomaz/analise_dados_cancer_br`
2.  **Instale as dependências:** `pip install -r requirements.txt`
3.  **Execute a aplicação:** `python run.py`
4.  **Acesse a aplicação:** No navegador, abra o endereço `http://127.0.0.1:5000/`

### Funcionalidades

*   **Página Inicial:** Apresenta um dashboard com cards para acesso às análises.
*   **Análise por Gênero:** Exibe a distribuição de diagnósticos de câncer por gênero.
*   **Distribuição de Idades:** Apresenta a distribuição de idades dos pacientes com câncer.
*   **Frequência de Doenças:** Mostra a frequência dos tipos de câncer mais comuns.
*   **Análise por Faixa Etária:** Exibe os tipos de câncer mais comuns por faixa etária.
*   **Análise de Câncer em Crianças e Adolescentes:** Apresenta a evolução dos tipos de câncer mais comuns em crianças e adolescentes ao longo do tempo.

### Resultados

Os resultados da análise podem ser visualizados na aplicação web. Alguns dos insights obtidos incluem:

*   Maior incidência de certos tipos de câncer em determinadas faixas etárias.
*   Variações na frequência de câncer ao longo do tempo em crianças e adolescentes.
*   Distribuição desigual de diagnósticos entre os gêneros.

### Próximos Passos

*   Explorar outras variáveis e relações nos dados.
*   Implementar modelos de machine learning para previsão de risco de câncer.
*   Melhorar a interface da aplicação web.

### Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

### Licença

Este projeto está sob a licença MIT.

**Observação:** Este README foi gerado com base nas informações fornecidas. É importante adaptá-lo e complementá-lo com informações específicas do seu projeto.
