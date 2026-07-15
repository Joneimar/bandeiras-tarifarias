"""Simulador de Impacto no Consumo."""

import streamlit as st
import pandas as pd

from src.api import (
    BANDEIRA_CORES,
    bandeira_atual,
    fetch_bandeiras,
    impacto_mensal,
)
from src.charts import (
    impacto_anual_acumulado,
    impacto_historico,
    impacto_mensal_medio,
)


@st.cache_data(ttl=3600, show_spinner=False)
def load_data() -> pd.DataFrame:
    return fetch_bandeiras()


with st.spinner("Carregando dados..."):
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.stop()

nome_band, custo_mwh, custo_kwh, data_ref = bandeira_atual(df)
cor_atual = BANDEIRA_CORES.get(nome_band, "#888")

st.markdown("# 💰 Simulador de Impacto no Consumo")
st.markdown(
    "Informe o consumo médio mensal da sua unidade consumidora para calcular "
    "o impacto financeiro histórico das bandeiras tarifárias."
)

st.divider()

# ── Perfis pré-definidos ─────────────────────────────────────────────────────
st.markdown("### Perfil de Consumo")

perfil = st.selectbox(
    "Selecione um perfil ou personalize os valores",
    [
        "Grupo A — Comercial (50 MWh/mês)",
        "Grupo A — Industrial médio (200 MWh/mês)",
        "Grupo A — Industrial grande (500 MWh/mês)",
        "Grupo B — Residencial (150 kWh/mês)",
        "Personalizado",
    ],
    index=0,
)

PERFIS_DEFAULT = {
    "Grupo A — Comercial (50 MWh/mês)": [50000] * 12,
    "Grupo A — Industrial médio (200 MWh/mês)": [200000] * 12,
    "Grupo A — Industrial grande (500 MWh/mês)": [500000] * 12,
    "Grupo B — Residencial (150 kWh/mês)": [150] * 12,
}

MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

if perfil == "Personalizado":
    defaults = [50000] * 12

    st.markdown("#### Consumo mensal (kWh)")
    st.caption("Ajuste os valores para cada mês.")

    consumo_df = pd.DataFrame({
        "Mês": MESES,
        "Consumo (kWh)": defaults,
    })

    edited = st.data_editor(
        consumo_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Mês": st.column_config.TextColumn("Mês", disabled=True, width="small"),
            "Consumo (kWh)": st.column_config.NumberColumn(
                "Consumo (kWh)",
                min_value=0,
                max_value=10_000_000,
                step=100,
                format="%d",
            ),
        },
        num_rows="fixed",
    )
    consumo_mensal = edited["Consumo (kWh)"].tolist()
else:
    consumo_mensal = PERFIS_DEFAULT[perfil]

consumo_medio = sum(consumo_mensal) / 12

st.divider()

# ── Cálculo de impacto ───────────────────────────────────────────────────────
df_impacto = impacto_mensal(df, consumo_mensal)

st.markdown("### Impacto Atual")

impacto_atual = custo_kwh * consumo_mensal[data_ref.month - 1]
impacto_anual_total = df_impacto[df_impacto["ano"] == data_ref.year]["impacto_rs"].sum()
impacto_total_hist = df_impacto["impacto_rs"].sum()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Bandeira Vigente</div>
        <div class="kpi-value">
            <span class="bandeira-badge" style="background:{cor_atual}">{nome_band}</span>
        </div>
        <div class="kpi-sub">Ref. {data_ref.strftime('%b/%Y')}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Impacto Este Mês</div>
        <div class="kpi-value" style="color:{cor_atual}">R$ {impacto_atual:,.2f}</div>
        <div class="kpi-sub">sobre {consumo_mensal[data_ref.month - 1]:,.0f} kWh</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Acumulado {data_ref.year}</div>
        <div class="kpi-value" style="color:#f59e0b">R$ {impacto_anual_total:,.2f}</div>
        <div class="kpi-sub">custo adicional no ano</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Histórico</div>
        <div class="kpi-value" style="color:#3b82f6">R$ {impacto_total_hist:,.2f}</div>
        <div class="kpi-sub">desde {int(df['ano'].min())}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

if consumo_medio >= 500:
    custo_anual_medio = (
        df_impacto.groupby("ano")["impacto_rs"].sum().mean()
    )
    st.success(
        f"💡 Com um consumo médio de **{consumo_medio:,.0f} kWh/mês**, sua unidade consumidora "
        f"paga em média **R$ {custo_anual_medio:,.2f}/ano** em adicionais de bandeiras tarifárias. "
        f"No **Ambiente de Contratação Livre (ACL)**, esse custo não existe — o que pode representar "
        f"maior previsibilidade e economia na conta de energia.",
        icon="⚡",
    )

st.divider()

st.markdown("### Análise Histórica do Impacto")

tab1, tab2, tab3 = st.tabs(["📊 Acumulado por Ano", "🗓️ Sazonalidade", "📈 Timeline"])

with tab1:
    st.plotly_chart(impacto_anual_acumulado(df_impacto), width="stretch")

with tab2:
    st.plotly_chart(impacto_mensal_medio(df_impacto), width="stretch")

with tab3:
    st.plotly_chart(impacto_historico(df_impacto), width="stretch")

with st.expander("📋 Tabela detalhada de impacto", expanded=False):
    tabela = (
        df_impacto[["data", "bandeira", "adicional_kwh", "consumo_kwh", "impacto_rs"]]
        .rename(columns={
            "data": "Data",
            "bandeira": "Bandeira",
            "adicional_kwh": "Adicional (R$/kWh)",
            "consumo_kwh": "Consumo (kWh)",
            "impacto_rs": "Impacto (R$)",
        })
        .sort_values("Data", ascending=False)
        .reset_index(drop=True)
    )
    st.dataframe(tabela, width="stretch", height=400)
