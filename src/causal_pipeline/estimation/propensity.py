"""Propensity score estimation.

PERSONA B — Implementar.

Idea:
    Propensity score: e(X) = P(T=1 | X).
    Es el ingrediente central para IPW y AIPW.

    Bajo unconfoundedness (T ⊥ Y(0), Y(1) | X), condicionar en e(X) es suficiente
    para identificar el efecto causal (Rosenbaum & Rubin, 1983).

Modelos a implementar:
    - Logistic regression (paramétrico, interpretable).
    - Random forest (no paramétrico, captura no-linealidades).

Diagnósticos críticos:
    - Overlap / common support: distribuciones de e(X) deben solaparse entre
      grupos tratado y control.
    - Calibración: predicciones de propensity deben ser bien calibradas.
    - Weights extremos: indica violación de positividad → considerar trimming.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

PropensityModel = Literal["logistic", "random_forest"]


def fit_propensity_score(
    df: pd.DataFrame,
    treatment: str,
    covariates: list[str],
    model: PropensityModel = "logistic",
    seed: int = 42,
) -> np.ndarray:
    """Estima e(X) = P(T=1 | X) para cada observación.

    Parameters
    ----------
    df : DataFrame.
    treatment : nombre de la columna del tratamiento (binario).
    covariates : variables explicativas para el modelo.
    model : tipo de modelo.
    seed : semilla.

    Returns
    -------
    array de propensity scores, uno por observación.
    """
    raise NotImplementedError("Persona B — implementar propensity score")


def check_overlap(
    propensity: np.ndarray,
    treatment: np.ndarray,
    threshold: float = 0.05,
) -> dict:
    """Diagnóstico de overlap entre grupos tratado y control.

    Returns
    -------
    dict con:
        - min_treated, max_treated, min_control, max_control
        - violation: True si hay propensity < threshold o > 1-threshold
        - n_extreme: número de observaciones con weights extremos
    """
    raise NotImplementedError("Persona B — implementar diagnóstico de overlap")


def trim_extreme_propensity(
    propensity: np.ndarray,
    threshold: float = 0.05,
) -> np.ndarray:
    """Trunca propensity scores extremos para estabilizar pesos IPW.

    Estrategia: clipear a [threshold, 1 - threshold].
    """
    raise NotImplementedError("Persona B — implementar trimming")
