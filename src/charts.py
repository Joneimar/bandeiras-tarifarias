"""Gráficos Plotly para o dashboard de Bandeiras Tarifárias."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.api import BANDEIRA_CORES, BANDEIRA_ORDEM

_LAYOUT_DEFAULTS = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=13),
    margin=dict(l=40, r=20, t=40, b=40),
    hoverlabel=dict(bgcolor="#1e1e2e", font_size=13),
)

MESES_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}


def _apply_layout(fig: go.Figure, **kwargs) -> go.Figure:
    merged = {**_LAYOUT_DEFAULTS, **kwargs}
    fig.update_layout(**merged)
    return fig


def timeline_bandeiras(df: pd.DataFrame) -> go.Figure:
    """Linha do tempo com custo adicional colorido pela bandeira acionada."""
    fig = go.Figure()

    for bandeira in BANDEIRA_ORDEM:
        subset = df[df["bandeira"] == bandeira]
        if subset.empty:
            continue
        fig.add_trace(go.Bar(
            x=subset["data"],
            y=subset["adicional_mwh"],
            name=bandeira,
            marker_color=BANDEIRA_CORES.get(bandeira, "#888"),
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                f"Bandeira: {bandeira}<br>"
                "Adicional: R$ %{y:.2f}/MWh"
                "<extra></extra>"
            ),
        ))

    return _apply_layout(
        fig,
        title="Histórico de Bandeiras Tarifárias",
        xaxis_title="",
        yaxis_title="Adicional (R$/MWh)",
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )


def distribuicao_bandeiras(resumo: pd.DataFrame) -> go.Figure:
    """Gráfico de rosca com a distribuição percentual de cada bandeira."""
    cores = [BANDEIRA_CORES.get(b, "#888") for b in resumo["bandeira"]]
    fig = go.Figure(go.Pie(
        labels=resumo["bandeira"],
        values=resumo["meses"],
        hole=0.55,
        marker=dict(colors=cores),
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>%{value} meses (%{percent})<extra></extra>",
    ))
    return _apply_layout(fig, title="Distribuição por Tipo de Bandeira", showlegend=False)


def custo_medio_por_ano(custo_anual: pd.DataFrame) -> go.Figure:
    """Barras horizontais do custo adicional médio por ano."""
    fig = go.Figure(go.Bar(
        x=custo_anual["custo_medio"],
        y=custo_anual["ano"].astype(str),
        orientation="h",
        marker_color="#3b82f6",
        hovertemplate="<b>%{y}</b><br>Custo médio: R$ %{x:.2f}/MWh<extra></extra>",
    ))
    return _apply_layout(
        fig,
        title="Custo Adicional Médio por Ano",
        xaxis_title="R$/MWh",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
    )


def heatmap_mensal(df: pd.DataFrame) -> go.Figure:
    """Heatmap: ano x mês com o valor do adicional tarifário."""
    pivot = df.pivot_table(
        index="ano", columns="mes", values="adicional_mwh", aggfunc="first"
    )
    pivot = pivot.reindex(columns=range(1, 13))

    labels_mes = [MESES_PT[m] for m in range(1, 13)]

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=labels_mes,
        y=pivot.index.astype(str),
        colorscale=[
            [0.0, "#22c55e"],
            [0.25, "#eab308"],
            [0.5, "#f97316"],
            [0.75, "#ef4444"],
            [1.0, "#991b1b"],
        ],
        colorbar=dict(title="R$/MWh"),
        hovertemplate="<b>%{y} — %{x}</b><br>Adicional: R$ %{z:.2f}/MWh<extra></extra>",
    ))
    return _apply_layout(
        fig,
        title="Mapa de Calor — Adicional Tarifário por Mês e Ano",
        yaxis=dict(autorange="reversed"),
    )


def bandeira_por_ano_empilhado(df: pd.DataFrame) -> go.Figure:
    """Barras empilhadas: meses de cada bandeira por ano."""
    contagem = (
        df.groupby(["ano", "bandeira"], observed=True)
        .size()
        .reset_index(name="meses")
    )

    fig = go.Figure()
    for bandeira in BANDEIRA_ORDEM:
        subset = contagem[contagem["bandeira"] == bandeira]
        if subset.empty:
            continue
        fig.add_trace(go.Bar(
            x=subset["ano"].astype(str),
            y=subset["meses"],
            name=bandeira,
            marker_color=BANDEIRA_CORES.get(bandeira, "#888"),
            hovertemplate="<b>%{x}</b><br>%{y} meses<extra></extra>",
        ))

    return _apply_layout(
        fig,
        title="Composição de Bandeiras por Ano",
        xaxis_title="",
        yaxis_title="Meses",
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
