"""Página 1 — Dashboard de Bandeiras Tarifárias."""

import streamlit as st
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
from src.style import inject_css, sidebar_footer

st.set_page_config(page_title="Dashboard — Bandeiras Tarifárias", page_icon="📊", layout="wide")
inject_css()

with st.sidebar:
    st.markdown("## 📊 Dashboard")
    st.caption("Análise histórica das bandeiras tarifárias.")
    sidebar_footer()


@st.cache_data(ttl=3600, show_spinner=False)
def load_data() -> pd.DataFrame:
    return fetch_bandeiras()


with st.spinner("Buscando dados na API da ANEEL..."):
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Não foi possível carregar os dados da ANEEL: {e}")
        st.stop()

nome_bandeira, custo_mwh, custo_kwh, data_ref = bandeira_atual(df)
cor_atual = BANDEIRA_CORES.get(nome_bandeira, "#888")

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 📊 Dashboard — Bandeiras Tarifárias")

st.divider()

# ── KPIs ─────────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)

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
        <div class="kpi-value" style="color:{cor_atual}">R$ {custo_mwh:.2f}/MWh</div>
        <div class="kpi-sub">R$ {custo_kwh:.5f}/kWh</div>
    </div>
    """, unsafe_allow_html=True)

total_meses = len(df)
ano_min, ano_max = int(df["ano"].min()), int(df["ano"].max())
with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Série Histórica</div>
        <div class="kpi-value" style="color:#3b82f6">{total_meses} meses</div>
        <div class="kpi-sub">{ano_min} – {ano_max}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ── Filtro ───────────────────────────────────────────────────────────────────
with st.expander("🔍 Filtrar período", expanded=False):
    sel_anos = st.slider("Intervalo de anos", ano_min, ano_max, (ano_min, ano_max))
    df_f = df[(df["ano"] >= sel_anos[0]) & (df["ano"] <= sel_anos[1])]
    st.caption(f"{len(df_f)} meses no período selecionado ({sel_anos[0]}–{sel_anos[1]})")

# ── Gráficos ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📈 Visão Geral", "🗓️ Análise Temporal", "📊 Distribuição"])

with tab1:
    st.plotly_chart(timeline_bandeiras(df_f), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            distribuicao_bandeiras(resumo_por_bandeira(df_f)),
            use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            custo_medio_por_ano(custo_medio_anual(df_f)),
            use_container_width=True,
        )

with tab2:
    st.plotly_chart(heatmap_mensal(df_f), use_container_width=True)
    st.plotly_chart(bandeira_por_ano_empilhado(df_f), use_container_width=True)

with tab3:
    resumo = resumo_por_bandeira(df_f)

    st.markdown("#### Resumo por Tipo de Bandeira")
    for _, row in resumo.iterrows():
        cor = BANDEIRA_CORES.get(row["bandeira"], "#888")
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:1rem; padding:0.75rem 1rem;
                    border-radius:8px; border:1px solid #2a2a32; background:#18181c; margin-bottom:0.5rem;">
            <div style="width:14px; height:14px; border-radius:50%; background:{cor}; flex-shrink:0;"></div>
            <div style="flex:1;">
                <strong>{row['bandeira']}</strong>
            </div>
            <div style="color:#a1a1aa;">
                {int(row['meses'])} meses ({row['percentual']}%)
            </div>
            <div style="width:120px; background:#2a2a32; border-radius:4px; height:8px;">
                <div style="width:{row['percentual']}%; background:{cor}; border-radius:4px; height:100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    with st.expander("📋 Tabela de dados completa", expanded=False):
        st.dataframe(
            df_f[["data", "bandeira", "adicional_mwh", "adicional_kwh"]]
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
