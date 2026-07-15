"""Estilos CSS compartilhados entre as páginas."""

import streamlit as st

CUSTOM_CSS = """
<style>
    [data-testid="stAppViewContainer"] { background-color: #0f0f13; }
    [data-testid="stSidebar"] { background-color: #141418; }
    [data-testid="stHeader"] { background-color: rgba(15,15,19,0.95); }

    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .sidebar-push { flex: 1; }

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
    .page-footer {
        text-align: center;
        color: #71717a;
        font-size: 0.85rem;
        padding: 1rem 0;
    }
    .page-footer a { color: #3b82f6; text-decoration: none; }
    .page-footer a:hover { text-decoration: underline; }

</style>
"""


def inject_css():
    """Injeta os estilos customizados na página."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def sidebar_footer():
    """Rodapé da sidebar empurrado para o fundo."""
    st.markdown('<div class="sidebar-push"></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption(
        "Desenvolvido por [Joneimar Lemos](https://energycode.com.br)  \n"
        "Dados: [ANEEL — Dados Abertos](https://dadosabertos.aneel.gov.br/)"
    )


def page_footer():
    """Rodapé centralizado para o final de cada página."""
    st.divider()
    st.markdown(
        '<div class="page-footer">'
        '⚡ Bandeiras Tarifárias · Desenvolvido por Joneimar Lemos · '
        '<a href="https://energycode.com.br" target="_blank">energycode.com.br</a>'
        '</div>',
        unsafe_allow_html=True,
    )
