# ⚡ Dashboard — Bandeiras Tarifárias do Setor Elétrico Brasileiro

Dashboard interativo que consome dados em tempo real da **API de Dados Abertos da ANEEL** para análise do histórico de bandeiras tarifárias no Brasil.

O sistema de bandeiras tarifárias, criado pela ANEEL em 2015, sinaliza mensalmente o custo de geração de energia elétrica. Quando as condições de geração são desfavoráveis (baixos níveis de reservatórios, despacho térmico elevado), bandeiras de maior custo são acionadas, impactando diretamente a conta de luz do consumidor.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-FF4B4B?logo=streamlit&logoColor=white)
![ANEEL](https://img.shields.io/badge/Dados-ANEEL_Abertos-009c3b)
![License](https://img.shields.io/badge/Licença-MIT-blue)

## Funcionalidades

- **Bandeira vigente** com custo adicional e impacto estimado na conta de luz.
- **Linha do tempo** do histórico completo de bandeiras desde 2015.
- **Distribuição percentual** por tipo de bandeira (Verde, Amarela, Vermelha P1/P2, Escassez Hídrica).
- **Custo adicional médio por ano** para análise de tendências.
- **Heatmap mensal** (ano × mês) para identificar padrões sazonais.
- **Composição por ano** com barras empilhadas.
- **Filtro interativo** por período.
- **Tabela exportável** com dados completos.
- **Seção metodológica** com contexto regulatório (REN 547/2013 e REN 2.939/2021).

## Pipeline de Dados

```
API ANEEL (CKAN)  →  Requisição SQL  →  Parsing (pandas)  →  Cache (1h)  →  Dashboard (Streamlit + Plotly)
```

1. Consulta SQL via endpoint `datastore_search_sql` da API CKAN da ANEEL.
2. Tratamento de tipos (`DatCompetencia` → datetime, `VlrAdicionalBandeira` → float).
3. Cache de 1 hora via `st.cache_data` para otimizar performance sem sobrecarregar a API.
4. Visualizações interativas com Plotly em tema escuro.

## Estrutura do Projeto

```
bandeiras-tarifarias/
├── app.py                 # App Streamlit principal
├── src/
│   ├── api.py             # Consumo da API ANEEL e transformações de dados
│   └── charts.py          # Gráficos Plotly (timeline, heatmap, distribuição)
├── requirements.txt       # Dependências
└── README.md
```

## Como Executar

```bash
# Clone o repositório
git clone https://github.com/Joneimar/bandeiras-tarifarias.git
cd bandeiras-tarifarias

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
```

## Tecnologias

| Tecnologia | Uso |
|---|---|
| **Python 3.10+** | Linguagem principal |
| **Streamlit** | Framework do dashboard |
| **pandas** | Manipulação e análise de dados |
| **Plotly** | Gráficos interativos |
| **requests** | Consumo da API REST da ANEEL |

## Fonte de Dados

[API de Dados Abertos da ANEEL](https://dadosabertos.aneel.gov.br/dataset/bandeiras-tarifarias) — recurso público com dados mensais de bandeiras tarifárias desde janeiro de 2015.

## Autor

**Joneimar Lemos** — Desenvolvedor & Analista de Dados no Setor Elétrico

- Portfólio: [energycode.com.br](https://energycode.com.br)
- LinkedIn: [linkedin.com/in/joneimar](https://linkedin.com/in/joneimar)

## Licença

MIT
