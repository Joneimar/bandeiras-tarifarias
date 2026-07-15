"""Dashboard — Bandeiras Tarifárias do Sistema Elétrico Brasileiro.

Dados consumidos em tempo real da API de Dados Abertos da ANEEL.
Desenvolvido por Joneimar Lemos · energycode.com.br
"""

import streamlit as st

st.set_page_config(
    page_title="Bandeiras Tarifárias — Setor Elétrico",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

import pandas as pd

from src.api import (
    BANDEIRA_CORES,
    bandeira_atual,
    custo_medio_anual,
    fetch_bandeiras,
    resumo_por_bandeira,
)
from src.charts import (
    bandeira_por_ano_empilhado,
    custo_medio_por_ano,
    distribuicao_bandeiras,
    heatmap_mensal,
    timeline_bandeiras,
)

# ── Estilo customizado ──────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0f0f13; }
    [data-testid="stSidebar"] { background-color: #141418; }
    .kpi-card {
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2a2a32;
        background: linear-gradient(135deg, #18181c 0%, #141418 100%);
        text-align: center;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #a1a1aa;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 0.85rem;
        color: #a1a1aa;
        margin-top: 0.35rem;
    }
    .bandeira-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.9rem;
        color: #fff;
    }
    .info-box {
        padding: 1.25rem;
        border-radius: 10px;
        border: 1px solid #2a2a32;
        background: #18181c;
        font-size: 0.9rem;
        color: #d4d4d8;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600, show_spinner=False)
def load_data() -> pd.DataFrame:
    return fetch_bandeiras()


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Bandeiras Tarifárias")
    st.caption("Dados: [ANEEL — Dados Abertos](https://dadosabertos.aneel.gov.br/)")

    st.markdown("---")

    st.markdown("""
    <div class="info-box">
        <strong>O que são Bandeiras Tarifárias?</strong><br><br>
        Sistema criado pela ANEEL em 2015 que sinaliza, mês a mês, o custo
        real de geração de energia elétrica no Brasil.<br><br>
        Quando os reservatórios estão cheios, a bandeira é
        <strong style="color:#22c55e">Verde</strong> (sem acréscimo).
        Em condições adversas, acionam-se as bandeiras
        <strong style="color:#eab308">Amarela</strong>,
        <strong style="color:#ef4444">Vermelha P1</strong>,
        <strong style="color:#991b1b">Vermelha P2</strong> ou
        <strong style="color:#7c3aed">Escassez Hídrica</strong>,
        com acréscimos progressivos na conta de luz.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "Desenvolvido por [Joneimar Lemos](https://energycode.com.br)  \n"
        "Dados atualizados via API da ANEEL"
    )


# ── Carregamento dos dados ───────────────────────────────────────────────────
with st.spinner("Buscando dados na API da ANEEL..."):
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Não foi possível carregar os dados da ANEEL: {e}")
        st.stop()

nome_bandeira, custo_mwh, custo_kwh, data_ref = bandeira_atual(df)
resumo = resumo_por_bandeira(df)
custo_anual = custo_medio_anual(df)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("# ⚡ Dashboard — Bandeiras Tarifárias")
st.markdown("Análise do histórico de bandeiras tarifárias do Sistema Elétrico Brasileiro, "
            "com dados em tempo real da API de Dados Abertos da ANEEL.")

st.markdown("---")

# ── KPIs ─────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

cor_atual = BANDEIRA_CORES.get(nome_bandeira, "#888")
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Bandeira Vigente</div>
        <div class="kpi-value">
            <span class="bandeira-badge" style="background:{cor_atual}">{nome_bandeira}</span>
        </div>
        <div class="kpi-sub">Ref. {data_ref.strftime('%b/%Y')}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Adicional Atual</div>
        <div class="kpi-value" style="color:{cor_atual}">R$ {custo_mwh:.2f}</div>
        <div class="kpi-sub">por MWh</div>
    </div>
    """, unsafe_allow_html=True)

consumo_medio_kwh = 150
custo_mensal = custo_kwh * consumo_medio_kwh
with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Impacto Mensal Estimado</div>
        <div class="kpi-value" style="color:{cor_atual}">R$ {custo_mensal:.2f}</div>
        <div class="kpi-sub">consumo residencial de {consumo_medio_kwh} kWh</div>
    </div>
    """, unsafe_allow_html=True)

total_meses = len(df)
ano_min, ano_max = int(df["ano"].min()), int(df["ano"].max())
with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Série Histórica</div>
        <div class="kpi-value" style="color:#3b82f6">{total_meses} meses</div>
        <div class="kpi-sub">{ano_min} – {ano_max}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ── Filtro de período ────────────────────────────────────────────────────────
with st.expander("🔍 Filtrar período", expanded=False):
    sel_anos = st.slider("Selecione o intervalo de anos", ano_min, ano_max, (ano_min, ano_max))
    df_filtrado = df[(df["ano"] >= sel_anos[0]) & (df["ano"] <= sel_anos[1])]
    st.caption(f"{len(df_filtrado)} meses no período selecionado ({sel_anos[0]}–{sel_anos[1]})")

# ── Gráficos principais ─────────────────────────────────────────────────────
st.plotly_chart(timeline_bandeiras(df_filtrado), use_container_width=True)

col_left, col_right = st.columns(2)

with col_left:
    st.plotly_chart(
        distribuicao_bandeiras(resumo_por_bandeira(df_filtrado)),
        use_container_width=True,
    )

with col_right:
    st.plotly_chart(
        custo_medio_por_ano(custo_medio_anual(df_filtrado)),
        use_container_width=True,
    )

st.plotly_chart(heatmap_mensal(df_filtrado), use_container_width=True)

st.plotly_chart(bandeira_por_ano_empilhado(df_filtrado), use_container_width=True)

# ── Tabela de dados ──────────────────────────────────────────────────────────
with st.expander("📋 Dados completos", expanded=False):
    st.dataframe(
        df_filtrado[["data", "bandeira", "adicional_mwh", "adicional_kwh"]]
        .rename(columns={
            "data": "Data",
            "bandeira": "Bandeira",
            "adicional_mwh": "Adicional (R$/MWh)",
            "adicional_kwh": "Adicional (R$/kWh)",
        })
        .sort_values("Data", ascending=False)
        .reset_index(drop=True),
        use_container_width=True,
        height=400,
    )

# ── Seção metodológica ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Sobre os Dados e a Metodologia")

st.markdown("""
**Fonte:** API de Dados Abertos da ANEEL — recurso
[Bandeiras Tarifárias](https://dadosabertos.aneel.gov.br/dataset/bandeiras-tarifarias).

**Pipeline de dados:**
1. Requisição paginada ao endpoint `datastore_search` da API CKAN da ANEEL.
2. Parsing e tipagem dos campos (`DatCompetencia` → datetime, `VlrAdicionalBandeira` → float em R$/MWh).
3. Conversão R$/MWh → R$/kWh para cálculos de impacto no consumidor residencial.
4. Cache de 1h via `st.cache_data` para otimizar re-renderizações sem sobrecarregar a API.

**Bandeiras disponíveis:**
| Bandeira | Condição | Acréscimo |
|---|---|---|
| 🟢 Verde | Condições favoráveis de geração | Sem acréscimo |
| 🟡 Amarela | Condições menos favoráveis | Acréscimo moderado |
| 🔴 Vermelha P1 | Condições desfavoráveis | Acréscimo elevado |
| 🔴 Vermelha P2 | Condições muito desfavoráveis | Acréscimo alto |
| 🟣 Escassez Hídrica | Crise hídrica severa (2021) | Acréscimo emergencial |

**Contexto regulatório:** O sistema de bandeiras tarifárias foi instituído pela Resolução Normativa
ANEEL nº 547/2013 e passou a vigorar em janeiro de 2015. A bandeira de Escassez Hídrica foi
criada pela Resolução nº 2.939/2021 para cobrir custos do acionamento emergencial de térmicas
durante a crise hídrica de 2021.
""")

st.markdown("---")
st.caption("⚡ Dashboard de Bandeiras Tarifárias · Desenvolvido por Joneimar Lemos · energycode.com.br")
