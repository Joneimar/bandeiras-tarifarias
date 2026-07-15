"""Estilos CSS compartilhados entre as páginas."""

import streamlit as st

CUSTOM_CSS = """
<style>
    [data-testid="stAppViewContainer"] { background-color: #0f0f13; }
    [data-testid="stSidebar"] { background-color: #141418; }
    [data-testid="stHeader"] { background-color: rgba(15,15,19,0.95); }

    .kpi-card {
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #2a2a32;
        background: linear-gradient(135deg, #18181c 0%, #141418 100%);
        text-align: center;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #a1a1aa;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #a1a1aa;
        margin-top: 0.25rem;
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
    .feature-card {
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2a2a32;
        background: #18181c;
        height: 100%;
    }
    .feature-card h4 {
        margin: 0 0 0.5rem 0;
        color: #f4f4f5;
    }
    .feature-card p {
        margin: 0;
        color: #a1a1aa;
        font-size: 0.9rem;
        line-height: 1.5;
    }
</style>
"""


def inject_css():
    """Injeta os estilos customizados na página."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def sidebar_footer():
    """Rodapé padrão da sidebar."""
    st.markdown("---")
    st.markdown(
        "Desenvolvido por [Joneimar Lemos](https://energycode.com.br)  \n"
        "Dados: [ANEEL — Dados Abertos](https://dadosabertos.aneel.gov.br/)"
    )
