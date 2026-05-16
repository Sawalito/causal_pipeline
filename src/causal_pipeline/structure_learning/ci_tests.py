"""Tests de independencia condicional para PC algorithm.

PERSONA A — Implementar las funciones de este módulo.

Tests requeridos:
    - Fisher Z: para variables continuas con dependencia lineal.
    - Chi-cuadrada: para variables discretas/categóricas.

Referencias:
    - Spirtes, Glymour, Scheines (2000), Causation, Prediction, and Search, Ch.5
    - Kalisch & Bühlmann (2007), "Estimating high-dimensional DAGs with the PC-algorithm"
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def fisher_z_test(
    df: pd.DataFrame,
    x: str,
    y: str,
    conditioning_set: list[str] | None = None,
    alpha: float = 0.05,
) -> tuple[bool, float]:
    """Test de independencia condicional vía Fisher Z (variables continuas).

    H0: X ⊥ Y | conditioning_set
    H1: X no ⊥ Y | conditioning_set

    Idea:
        1. Calcular correlación parcial entre X e Y dado conditioning_set.
        2. Aplicar transformación Z de Fisher.
        3. Comparar estadístico contra distribución normal.

    Parameters
    ----------
    df : DataFrame con las variables.
    x, y : nombres de las variables a testear.
    conditioning_set : variables sobre las que condicionar (puede ser vacío o None).
    alpha : nivel de significancia.

    Returns
    -------
    (independent, p_value): si rechazamos H0 → independent=False.
    """
    raise NotImplementedError("Persona A — implementar Fisher Z")


def chi_square_test(
    df: pd.DataFrame,
    x: str,
    y: str,
    conditioning_set: list[str] | None = None,
    alpha: float = 0.05,
) -> tuple[bool, float]:
    """Test de independencia condicional vía chi-cuadrada (variables discretas).

    Parameters
    ----------
    df : DataFrame con las variables (discretas).
    x, y : nombres de las variables.
    conditioning_set : variables sobre las que condicionar.
    alpha : nivel de significancia.

    Returns
    -------
    (independent, p_value)
    """
    raise NotImplementedError("Persona A — implementar chi-square")


def auto_ci_test(
    df: pd.DataFrame,
    x: str,
    y: str,
    conditioning_set: list[str] | None = None,
    alpha: float = 0.05,
) -> tuple[bool, float]:
    """Selecciona automáticamente Fisher Z o chi-cuadrada según los tipos.

    Heurística:
        - Si todas las variables involucradas son numéricas → Fisher Z.
        - Si hay variables categóricas → chi-cuadrada (discretizar las continuas).
    """
    raise NotImplementedError("Persona A — implementar auto-selector")
