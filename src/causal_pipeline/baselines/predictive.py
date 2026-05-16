"""Baseline predictivo puro (Random Forest).

PERSONA C — Implementar.

Propósito narrativo:
    Demostrar que un modelo puramente predictivo (que aprende P(Y | T, X) sin
    consideración causal) puede dar estimaciones SESGADAS del efecto causal,
    incluso si su error predictivo es bajo.

Comparación:
    - Random Forest predice Y dado (T, X).
    - "Efecto" estimado = predicción promedio con T=1 menos predicción con T=0.
    - Si hay confounding y no se ajusta correctamente, este "efecto" no es ATE.

Esto contrasta con AIPW que SÍ identifica el ATE bajo unconfoundedness.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class PredictiveBaselineResult:
    """Resultado del baseline predictivo."""

    pseudo_ate: float
    mse_train: float
    mse_test: float
    feature_importances: dict[str, float]


def random_forest_baseline(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    covariates: list[str],
    test_size: float = 0.2,
    seed: int = 42,
) -> PredictiveBaselineResult:
    """Baseline predictivo: estima un "efecto" como diferencia de predicciones.

    Pasos:
        1. Entrenar RF con features = covariates + treatment.
        2. Predecir Y_hat con T=1 para todos vs T=0 para todos.
        3. pseudo_ATE = mean(Y_hat_T=1 - Y_hat_T=0).

    Esto NO es un ATE válido en general. Sirve para mostrar el contraste con AIPW.
    """
    raise NotImplementedError("Persona C — implementar baseline predictivo")


def simpsons_paradox_demo(seed: int = 42) -> dict:
    """Genera un dataset sintético donde Simpson's paradox aparece.

    Construye un SCM tal que:
        - El efecto agregado de T sobre Y parece positivo.
        - Condicionando en el confounder correcto, el efecto es negativo (o viceversa).

    Returns
    -------
    dict con:
        - df: DataFrame del experimento sintético.
        - dag: DAG verdadero.
        - true_ate: ATE verdadero (computado analíticamente del SCM).
        - naive_estimate: estimación sin ajustar (regresión simple).
        - adjusted_estimate: estimación ajustada.
    """
    raise NotImplementedError("Persona C — implementar demo de Simpson's paradox")
