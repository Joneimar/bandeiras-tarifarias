"""Consumo da API de Dados Abertos da ANEEL — Bandeiras Tarifárias."""

from __future__ import annotations

import pandas as pd
import requests

_RESOURCE_ID = "0591b8f6-fe54-437b-b72b-1aa2efd46e42"
_BASE_URL = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search"

BANDEIRA_CORES: dict[str, str] = {
    "Verde": "#22c55e",
    "Amarela": "#eab308",
    "Vermelha P1": "#ef4444",
    "Vermelha P2": "#991b1b",
    "Escassez Hdrica": "#7c3aed",
    "Escassez Hídrica": "#7c3aed",
}

BANDEIRA_ORDEM: list[str] = [
    "Verde",
    "Amarela",
    "Vermelha P1",
    "Vermelha P2",
    "Escassez Hdrica",
]


def fetch_bandeiras() -> pd.DataFrame:
    """Busca o histórico completo de bandeiras tarifárias na API da ANEEL.

    Usa o endpoint datastore_search com paginação para obter todos os registros.

    Returns
    -------
    pd.DataFrame
        Colunas: data, bandeira, adicional_mwh (R$/MWh), adicional_kwh (R$/kWh).
    """
    records: list[dict] = []
    offset = 0
    limit = 500

    while True:
        resp = requests.get(
            _BASE_URL,
            params={
                "resource_id": _RESOURCE_ID,
                "limit": limit,
                "offset": offset,
            },
            timeout=30,
        )
        resp.raise_for_status()
        result = resp.json()["result"]
        batch = result["records"]
        records.extend(batch)
        if len(batch) < limit:
            break
        offset += limit

    df = pd.DataFrame(records)

    df["data"] = pd.to_datetime(df["DatCompetencia"])
    df["bandeira"] = df["NomBandeiraAcionada"].str.strip()
    df["adicional_mwh"] = (
        df["VlrAdicionalBandeira"]
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
    df["adicional_kwh"] = df["adicional_mwh"] / 1000

    df = (
        df[["data", "bandeira", "adicional_mwh", "adicional_kwh"]]
        .sort_values("data")
        .reset_index(drop=True)
    )

    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month

    return df


def bandeira_atual(df: pd.DataFrame) -> tuple[str, float, float, pd.Timestamp]:
    """Retorna a bandeira vigente (nome, custo R$/MWh, custo R$/kWh, data)."""
    ultimo = df.iloc[-1]
    return ultimo["bandeira"], ultimo["adicional_mwh"], ultimo["adicional_kwh"], ultimo["data"]


def resumo_por_bandeira(df: pd.DataFrame) -> pd.DataFrame:
    """Contagem e percentual de meses por tipo de bandeira."""
    contagem = (
        df.groupby("bandeira", observed=True)
        .size()
        .reset_index(name="meses")
    )
    contagem["percentual"] = (contagem["meses"] / contagem["meses"].sum() * 100).round(1)
    return contagem.sort_values("meses", ascending=False).reset_index(drop=True)


def custo_medio_anual(df: pd.DataFrame) -> pd.DataFrame:
    """Custo adicional médio por ano em R$/MWh."""
    return (
        df.groupby("ano", observed=True)["adicional_mwh"]
        .mean()
        .reset_index()
        .rename(columns={"adicional_mwh": "custo_medio"})
    )
