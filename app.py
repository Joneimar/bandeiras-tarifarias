"""Bandeiras Tarifárias — Entrypoint.

Orquestra a navegação entre páginas e aplica configurações globais.
"""

import streamlit as st
from src.style import inject_css, page_footer

st.set_page_config(
    page_title="Bandeiras Tarifárias — Setor Elétrico",
    page_icon="⚡",
    layout="wide",
)

inject_css()

pages = [
    st.Page("pages/pagina_inicial.py", title="Página Inicial", icon="⚡"),
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
    st.Page("pages/simulador.py", title="Simulador de Impacto", icon="💰"),
    st.Page("pages/metodologia.py", title="Dados e Metodologia", icon="📋"),
]

nav = st.navigation(pages, position="top")
nav.run()

page_footer()
