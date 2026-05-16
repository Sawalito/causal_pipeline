"""Carga del dataset Lalonde.

Lalonde (1986) — NSW experiment + observational comparison.
Variables canónicas:
    treat    : tratamiento binario (1 = recibió programa de capacitación)
    age      : edad en años
    educ     : años de educación
    black    : 1 si afroamericano
    hispan   : 1 si hispano
    married  : 1 si casado
    nodegree : 1 si no completó high school
    re74     : ingresos reales en 1974 (USD)
    re75     : ingresos reales en 1975 (USD)
    re78     : ingresos reales en 1978 (OUTCOME, USD)

Benchmark experimental: ATE ≈ $1,794 USD (Dehejia & Wahba, 1999).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

LALONDE_URL = "https://users.nber.org/~rdehejia/data/nsw_dw.dta"
DATA_DIR = Path(__file__).resolve().parents[3] / "data"

TREATMENT_COL = "treat"
OUTCOME_COL = "re78"
COVARIATES = ["age", "educ", "black", "hispan", "married", "nodegree", "re74", "re75"]


def load_lalonde(use_cache: bool = True) -> pd.DataFrame:
    """Carga el dataset Lalonde (versión Dehejia-Wahba experimental).

    Intenta primero la caché local en `data/lalonde.csv`, después la librería
    `causaldata` si está instalada, y finalmente descarga desde NBER.

    Parameters
    ----------
    use_cache : si True, prefiere la versión local antes de descargar.

    Returns
    -------
    DataFrame con columnas estandarizadas listas para el pipeline.
    """
    cache_path = DATA_DIR / "lalonde.csv"

    if use_cache and cache_path.exists():
        df = pd.read_csv(cache_path)
        return _validate(df)

    # Intentar causaldata primero (más limpio)
    try:
        from causaldata import nsw_mixtape  # type: ignore

        df = nsw_mixtape.load_pandas().data
    except ImportError:
        # Fallback: descarga directa desde NBER
        df = pd.read_stata(LALONDE_URL)

    df = _standardize_columns(df)
    df = _validate(df)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache_path, index=False)

    return df


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renombra columnas a las convenciones del proyecto."""
    rename_map = {
        "data_id": None,  # eliminar si existe
        "education": "educ",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if v is not None})
    if "data_id" in df.columns:
        df = df.drop(columns=["data_id"])
    return df


def _validate(df: pd.DataFrame) -> pd.DataFrame:
    """Verifica que las columnas esperadas estén presentes."""
    expected = [TREATMENT_COL, OUTCOME_COL] + COVARIATES
    missing = [c for c in expected if c not in df.columns]
    if missing:
        raise ValueError(f"Columnas faltantes en Lalonde: {missing}. Columnas presentes: {list(df.columns)}")
    # Convertir a tipos correctos
    df[TREATMENT_COL] = df[TREATMENT_COL].astype(int)
    return df[expected].copy()


def split_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Conveniencia: separa covariables, tratamiento y outcome.

    Returns
    -------
    X, t, y
    """
    return df[COVARIATES], df[TREATMENT_COL], df[OUTCOME_COL]
