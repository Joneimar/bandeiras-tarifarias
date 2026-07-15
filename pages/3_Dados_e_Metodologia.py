"""Página 3 — Dados e Metodologia."""

import streamlit as st

from src.style import inject_css, sidebar_footer

st.set_page_config(page_title="Dados e Metodologia — Bandeiras", page_icon="📋", layout="wide")
inject_css()

with st.sidebar:
    st.markdown("## 📋 Dados e Metodologia")
    st.caption("Fonte de dados, pipeline e referências.")
    sidebar_footer()

st.markdown("# 📋 Dados e Metodologia")
st.divider()

# ── Fonte de dados ───────────────────────────────────────────────────────────
st.markdown("## Fonte de Dados")

st.markdown("""
Os dados são consumidos em **tempo real** diretamente da
**[API de Dados Abertos da ANEEL](https://dadosabertos.aneel.gov.br/dataset/bandeiras-tarifarias)**
(Agência Nacional de Energia Elétrica).

O recurso utilizado é o dataset de **Bandeiras Tarifárias**, que contém registros mensais
desde janeiro de 2015 com os seguintes campos:
""")

st.markdown("""
| Campo | Descrição |
|---|---|
| `DatCompetencia` | Data de referência (mês/ano) |
| `NomBandeiraAcionada` | Tipo de bandeira acionada (Verde, Amarela, Vermelha P1, Vermelha P2, Escassez Hídrica) |
| `VlrAdicionalBandeira` | Valor do acréscimo tarifário (R$/MWh) |
""")

st.divider()

# ── Pipeline ETL ─────────────────────────────────────────────────────────────
st.markdown("## Pipeline ETL")

st.markdown("""
```
API ANEEL (CKAN)  →  Requisição paginada  →  Parsing (pandas)  →  Cache 1h  →  Dashboard
```
""")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="feature-card">
        <h4>1. Extração</h4>
        <p>Requisição paginada ao endpoint <code>datastore_search</code> da API CKAN da ANEEL
        com resource_id do dataset de bandeiras.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <h4>2. Transformação</h4>
        <p>Conversão de tipos: <code>DatCompetencia</code> → datetime,
        <code>VlrAdicionalBandeira</code> → float. Normalização de nomes
        e conversão R$/MWh → R$/kWh.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <h4>3. Cache</h4>
        <p>Cache de 1 hora via <code>st.cache_data</code> para otimizar
        re-renderizações sem sobrecarregar a API pública.</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="feature-card">
        <h4>4. Visualização</h4>
        <p>Gráficos interativos com Plotly em tema escuro.
        Filtros de período e seleção de submercado.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Estrutura do código ──────────────────────────────────────────────────────
st.markdown("## Estrutura do Projeto")

st.code("""
bandeiras-tarifarias/
├── app.py                              # Página inicial (Sobre)
├── pages/
│   ├── 1_📊_Dashboard.py              # Dashboard com gráficos
│   ├── 2_💰_Simulador_de_Impacto.py   # Simulador de custo
│   └── 3_📋_Dados_e_Metodologia.py    # Esta página
├── src/
│   ├── api.py                          # Consumo da API ANEEL + transformações
│   ├── charts.py                       # Gráficos Plotly
│   └── style.py                        # Estilos CSS compartilhados
├── .streamlit/
│   └── config.toml                     # Tema escuro fixo
├── requirements.txt
└── README.md
""", language="text")

st.divider()

# ── Tecnologias ──────────────────────────────────────────────────────────────
st.markdown("## Tecnologias")

st.markdown("""
| Tecnologia | Versão | Uso |
|---|---|---|
| **Python** | 3.10+ | Linguagem principal |
| **Streamlit** | ≥ 1.45 | Framework do dashboard multi-página |
| **pandas** | ≥ 2.2 | Manipulação e análise de dados |
| **Plotly** | ≥ 6.0 | Gráficos interativos |
| **requests** | ≥ 2.32 | Consumo da API REST da ANEEL |
""")

st.divider()

# ── Bandeiras ────────────────────────────────────────────────────────────────
st.markdown("## Referência das Bandeiras")

st.markdown("""
| Bandeira | Condição | Acréscimo | Cor |
|---|---|---|---|
| 🟢 Verde | Condições favoráveis de geração hidrelétrica | Sem acréscimo | Verde |
| 🟡 Amarela | Condições menos favoráveis | Acréscimo moderado | Amarelo |
| 🔴 Vermelha P1 | Condições desfavoráveis — acionamento de térmicas | Acréscimo elevado | Vermelho |
| 🔴 Vermelha P2 | Condições muito desfavoráveis — custo intensivo | Acréscimo alto | Vermelho escuro |
| 🟣 Escassez Hídrica | Crise hídrica severa (2021) | Acréscimo emergencial | Roxo |
""")

st.divider()

# ── Referências regulatórias ─────────────────────────────────────────────────
st.markdown("## Referências Regulatórias")

st.markdown("""
- **Resolução Normativa ANEEL nº 547/2013** — Estabelece as condições de aplicação do sistema
  de bandeiras tarifárias, definindo os patamares e as condições de acionamento.

- **Resolução ANEEL nº 2.939/2021** — Cria a bandeira tarifária de **Escassez Hídrica**,
  com acréscimo de R$ 14,20/100kWh, para cobrir custos do acionamento emergencial de
  usinas termelétricas durante a crise hídrica de 2021.

- **Resolução ANEEL nº 2.927/2020** — Instituiu o PLD horário a partir de janeiro de 2021,
  substituindo o PLD semanal. Embora aplicável ao PLD, impacta indiretamente o despacho
  térmico e consequentemente o acionamento de bandeiras.

- **Lei nº 12.783/2013** — Marco regulatório que, entre outras disposições, possibilitou
  a criação do sistema de bandeiras tarifárias.

- **API de Dados Abertos da ANEEL** — [dadosabertos.aneel.gov.br](https://dadosabertos.aneel.gov.br/)
  — Portal público com datasets acessíveis via API CKAN.
""")

st.divider()
st.caption("⚡ Bandeiras Tarifárias · Desenvolvido por Joneimar Lemos · [energycode.com.br](https://energycode.com.br)")
