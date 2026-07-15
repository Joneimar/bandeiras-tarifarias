"""Gráficos Plotly para o dashboard de Bandeiras Tarifárias."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from src.api import BANDEIRA_CORES, BANDEIRA_ORDEM

_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=13),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(bgcolor="#1e1e2e", font_size=13),
)

MESES_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}


def _apply(fig: go.Figure, **kw) -> go.Figure:
    fig.update_layout(**{**_LAYOUT, **kw})
    return fig


def timeline_bandeiras(df: pd.DataFrame) -> go.Figure:
    """Linha do tempo com custo adicional por bandeira.

    Verde aparece como marcador no eixo zero para meses sem acréscimo.
    """
    fig = go.Figure()

    verde = df[df["bandeira"] == "Verde"]
    if not verde.empty:
        fig.add_trace(go.Scatter(
            x=verde["data"],
            y=[0] * len(verde),
            mode="markers",
            name="Verde",
            marker=dict(color=BANDEIRA_CORES["Verde"], size=8, symbol="diamond"),
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Bandeira: Verde<br>"
                "Adicional: R$ 0,00/MWh"
                "<extra></extra>"
            ),
        ))

    for bandeira in BANDEIRA_ORDEM:
        if bandeira == "Verde":
            continue
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

    return _apply(
        fig,
        title="Histórico de Bandeiras Tarifárias",
        xaxis_title="",
        yaxis_title="Adicional (R$/MWh)",
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )


def distribuicao_bandeiras(resumo: pd.DataFrame) -> go.Figure:
    """Gráfico de rosca com a distribuição percentual."""
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
    return _apply(fig, title="Distribuição por Tipo de Bandeira", showlegend=False)


def custo_medio_por_ano(custo_anual: pd.DataFrame) -> go.Figure:
    """Barras horizontais do custo médio por ano.

    Valores zero recebem uma barra mínima visível com anotação.
    """
    custo = custo_anual.sort_values("ano").copy()

    y_display = custo["custo_medio"].apply(lambda v: max(v, 0.8))
    zeros = custo[custo["custo_medio"] == 0]

    fig = go.Figure(go.Bar(
        x=y_display,
        y=custo["ano"].astype(str),
        orientation="h",
        marker_color="#3b82f6",
        text=custo["custo_medio"].apply(lambda v: f"R$ {v:.2f}"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Custo médio: R$ %{customdata:.2f}/MWh<extra></extra>",
        customdata=custo["custo_medio"],
    ))

    for _, row in zeros.iterrows():
        fig.add_annotation(
            x=2.5,
            y=str(int(row["ano"])),
            text="R$ 0,00 (100% Verde)",
            showarrow=False,
            font=dict(size=11, color="#22c55e"),
            xanchor="left",
        )

    return _apply(
        fig,
        title="Custo Adicional Médio por Ano",
        xaxis_title="R$/MWh",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
    )


def heatmap_mensal(df: pd.DataFrame) -> go.Figure:
    """Heatmap: ano x mês com o valor do adicional."""
    pivot = df.pivot_table(index="ano", columns="mes", values="adicional_mwh", aggfunc="first")
    pivot = pivot.reindex(columns=range(1, 13)).sort_index()

    labels_mes = [MESES_PT[m] for m in range(1, 13)]

    hover_text = []
    for ano_idx in range(len(pivot)):
        row = []
        for mes_idx in range(12):
            val = pivot.iloc[ano_idx, mes_idx]
            if pd.isna(val):
                row.append("")
            else:
                bandeira_row = df[(df["ano"] == pivot.index[ano_idx]) & (df["mes"] == mes_idx + 1)]
                nome = bandeira_row.iloc[0]["bandeira"] if not bandeira_row.empty else ""
                row.append(f"<b>{pivot.index[ano_idx]} — {labels_mes[mes_idx]}</b><br>"
                          f"Bandeira: {nome}<br>Adicional: R$ {val:.2f}/MWh")
        hover_text.append(row)

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
        hovertext=hover_text,
        hovertemplate="%{hovertext}<extra></extra>",
    ))
    return _apply(
        fig,
        title="Mapa de Calor — Adicional Tarifário por Mês e Ano",
        yaxis=dict(autorange="reversed"),
    )


def bandeira_por_ano_empilhado(df: pd.DataFrame) -> go.Figure:
    """Barras empilhadas: meses de cada bandeira por ano, em ordem cronológica."""
    contagem = (
        df.groupby(["ano", "bandeira"], observed=True)
        .size()
        .reset_index(name="meses")
    )

    anos_ordenados = sorted(contagem["ano"].unique())

    fig = go.Figure()
    for bandeira in BANDEIRA_ORDEM:
        subset = contagem[contagem["bandeira"] == bandeira]
        if subset.empty:
            continue
        subset_sorted = subset.set_index("ano").reindex(anos_ordenados).fillna(0).reset_index()
        fig.add_trace(go.Bar(
            x=[str(a) for a in anos_ordenados],
            y=subset_sorted["meses"],
            name=bandeira,
            marker_color=BANDEIRA_CORES.get(bandeira, "#888"),
            hovertemplate="<b>%{x}</b><br>%{y:.0f} meses<extra>" + bandeira + "</extra>",
        ))

    return _apply(
        fig,
        title="Composição de Bandeiras por Ano",
        xaxis_title="",
        yaxis_title="Meses",
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )


# ── Gráficos de impacto no consumo ──────────────────────────────────────────

def impacto_historico(df_impacto: pd.DataFrame) -> go.Figure:
    """Timeline do impacto financeiro (R$) sobre o consumo do usuário."""
    fig = go.Figure()

    for bandeira in BANDEIRA_ORDEM:
        subset = df_impacto[df_impacto["bandeira"] == bandeira]
        if subset.empty:
            continue
        if bandeira == "Verde":
            fig.add_trace(go.Scatter(
                x=subset["data"],
                y=subset["impacto_rs"],
                mode="markers",
                name="Verde",
                marker=dict(color=BANDEIRA_CORES["Verde"], size=7, symbol="diamond"),
                hovertemplate=(
                    "<b>%{x|%b %Y}</b><br>"
                    "Impacto: R$ %{y:.2f}<br>"
                    "Consumo: %{customdata:.0f} kWh"
                    "<extra>Verde</extra>"
                ),
                customdata=subset["consumo_kwh"],
            ))
        else:
            fig.add_trace(go.Bar(
                x=subset["data"],
                y=subset["impacto_rs"],
                name=bandeira,
                marker_color=BANDEIRA_CORES.get(bandeira, "#888"),
                hovertemplate=(
                    "<b>%{x|%b %Y}</b><br>"
                    "Impacto: R$ %{y:.2f}<br>"
                    "Consumo: %{customdata:.0f} kWh"
                    "<extra>" + bandeira + "</extra>"
                ),
                customdata=subset["consumo_kwh"],
            ))

    return _apply(
        fig,
        title="Impacto Financeiro das Bandeiras no Seu Consumo",
        xaxis_title="",
        yaxis_title="Custo adicional (R$)",
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )


def impacto_anual_acumulado(df_impacto: pd.DataFrame) -> go.Figure:
    """Custo adicional acumulado por ano."""
    anual = (
        df_impacto.groupby("ano")["impacto_rs"]
        .sum()
        .reset_index()
        .sort_values("ano")
    )
    anual["impacto_rs"] = anual["impacto_rs"].round(2)

    fig = go.Figure(go.Bar(
        x=anual["ano"].astype(str),
        y=anual["impacto_rs"],
        marker_color="#3b82f6",
        text=anual["impacto_rs"].apply(lambda v: f"R$ {v:,.2f}"),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Custo adicional acumulado: R$ %{y:,.2f}<extra></extra>",
    ))

    return _apply(
        fig,
        title="Custo Adicional Acumulado por Ano",
        xaxis_title="",
        yaxis_title="R$",
    )


def impacto_mensal_medio(df_impacto: pd.DataFrame) -> go.Figure:
    """Impacto médio por mês do ano (sazonalidade)."""
    mensal = (
        df_impacto.groupby("mes")["impacto_rs"]
        .mean()
        .reset_index()
        .sort_values("mes")
    )

    labels = [MESES_PT[m] for m in mensal["mes"]]

    fig = go.Figure(go.Bar(
        x=labels,
        y=mensal["impacto_rs"].round(2),
        marker_color="#f59e0b",
        hovertemplate="<b>%{x}</b><br>Impacto médio: R$ %{y:.2f}<extra></extra>",
    ))

    return _apply(
        fig,
        title="Impacto Médio por Mês (Sazonalidade)",
        xaxis_title="",
        yaxis_title="Impacto médio (R$)",
    )
