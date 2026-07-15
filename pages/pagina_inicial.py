"""Página Inicial — Sobre o sistema de bandeiras tarifárias."""

import streamlit as st
from src.api import BANDEIRA_CORES, BANDEIRA_EMOJI, BANDEIRA_ORDEM

st.markdown("# ⚡ Bandeiras Tarifárias do Setor Elétrico Brasileiro")
st.markdown(
    "Dashboard analítico com dados em tempo real da **API de Dados Abertos da ANEEL** "
    "para análise do histórico de bandeiras tarifárias, impacto no custo de energia "
    "e simulação sobre o consumo."
)

st.divider()

# ── O que são Bandeiras Tarifárias ───────────────────────────────────────────
st.markdown("## O que são Bandeiras Tarifárias?")

st.markdown("""
O sistema de **Bandeiras Tarifárias** foi criado pela ANEEL (Agência Nacional de Energia Elétrica)
e passou a vigorar em **janeiro de 2015**. Ele funciona como um sinal de preço que indica, mês a mês,
o **custo real de geração de energia elétrica** no Brasil.

Quando as condições de geração são favoráveis — reservatórios cheios e geração hidrelétrica abundante —
a bandeira é **Verde** e não há acréscimo na conta. Quando as condições são adversas e é necessário
acionar usinas termelétricas (mais caras), bandeiras de maior custo são acionadas.
""")

st.markdown("")

cols = st.columns(5)
bandeira_info = {
    "Verde": "Condições favoráveis de geração. <b>Sem acréscimo</b> na tarifa.",
    "Amarela": "Condições menos favoráveis. Acréscimo <b>moderado</b> na tarifa.",
    "Vermelha P1": "Condições desfavoráveis. Acréscimo <b>elevado</b> — acionamento de térmicas.",
    "Vermelha P2": "Condições muito desfavoráveis. Acréscimo <b>alto</b> — custo intensivo de geração.",
    "Escassez Hídrica": "Crise hídrica severa (criada em 2021). Acréscimo <b>emergencial</b>.",
}

for i, bandeira in enumerate(BANDEIRA_ORDEM):
    with cols[i]:
        cor = BANDEIRA_CORES[bandeira]
        emoji = BANDEIRA_EMOJI[bandeira]
        st.markdown(f"""
        <div class="feature-card" style="text-align:center; border-top: 3px solid {cor};">
            <h4 style="font-size:1.5rem; margin-bottom:0.3rem;">{emoji}</h4>
            <h4 style="font-size:0.95rem;">{bandeira}</h4>
            <p style="font-size:0.82rem;">{bandeira_info[bandeira]}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

with st.expander("📜 Contexto Regulatório", expanded=False):
    st.markdown("""
    - **Resolução Normativa ANEEL nº 547/2013** — Instituiu o sistema de bandeiras tarifárias.
    - **Janeiro de 2015** — Início da vigência do sistema.
    - **Resolução ANEEL nº 2.939/2021** — Criou a bandeira de **Escassez Hídrica** para cobrir custos
      do acionamento emergencial de térmicas durante a crise hídrica de 2021.
    - O valor do adicional é definido mensalmente pela ANEEL e incide sobre cada kWh consumido
      pelos consumidores cativos (conectados à distribuidora).
    - Consumidores do **mercado livre de energia** não pagam bandeiras, mas estão expostos ao PLD.
    """)

st.divider()

st.markdown("## Como Usar este Dashboard")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
        <h4>📊 Dashboard</h4>
        <p>Visualize o histórico completo de bandeiras desde 2015 com gráficos interativos:
        timeline, heatmap, custo médio anual e composição por ano.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <h4>💰 Simulador de Impacto</h4>
        <p>Informe o consumo mensal da sua unidade consumidora e veja o impacto financeiro
        histórico das bandeiras tarifárias sobre o seu consumo.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <h4>📋 Dados e Metodologia</h4>
        <p>Detalhes sobre a fonte de dados (API ANEEL), pipeline ETL,
        estrutura do código e referências regulatórias.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.info(
    "👈 **Navegue pelas páginas** usando o menu lateral para acessar o Dashboard, "
    "o Simulador de Impacto ou os Dados e Metodologia.",
    icon="💡",
)
