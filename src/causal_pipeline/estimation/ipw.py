"""IPW (Inverse Propensity Weighting) estimator.

PERSONA B — Implementar.

Estimador de Horvitz-Thompson para ATE:

    ATE_IPW = (1/n) Σ [ T_i Y_i / e(X_i) - (1-T_i) Y_i / (1 - e(X_i)) ]

Variante estabilizada (Hajek):

    ATE_IPW_stab = Σ [T_i Y_i / e(X_i)] / Σ [T_i / e(X_i)]
                 - Σ [(1-T_i) Y_i / (1-e(X_i))] / Σ [(1-T_i) / (1-e(X_i))]

CI vía bootstrap no paramétrico (B = 1000).
"""

from __future__ import annotations

import pandas as pd

from causal_pipeline.interfaces import ATEResult, CausalDAG


def estimate_ate_ipw(
    df: pd.DataFrame,
    dag: CausalDAG,
    treatment: str,
    outcome: str,
    stabilized: bool = True,
    n_bootstrap: int = 1000,
    propensity_model: str = "logistic",
    trim_threshold: float = 0.05,
    seed: int = 42,
) -> ATEResult:
    """Estimación IPW del ATE.

    Pasos:
        1. Encontrar adjustment set via backdoor criterion.
        2. Estimar propensity score con las covariables del adjustment set.
        3. Diagnosticar overlap; aplicar trimming si es necesario.
        4. Calcular IPW (estabilizado o no).
        5. Bootstrap para CI.

    Parameters
    ----------
    df : DataFrame.
    dag : DAG causal.
    treatment, outcome : nombres de columnas.
    stabilized : usar versión estabilizada (Hajek).
    n_bootstrap : muestras bootstrap.
    propensity_model : modelo para e(X).
    trim_threshold : umbral para trimming de propensity extremo.
    seed : semilla.

    Returns
    -------
    ATEResult.
    """
    raise NotImplementedError("Persona B — implementar IPW")
