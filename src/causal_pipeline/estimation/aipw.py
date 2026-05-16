"""AIPW (Augmented IPW, doubly robust) estimator.

PERSONA B — Implementar.

Estimador doblemente robusto:

    ATE_AIPW = (1/n) Σ {
        [T_i (Y_i - μ_1(X_i)) / e(X_i)] + μ_1(X_i)
      - [(1-T_i) (Y_i - μ_0(X_i)) / (1-e(X_i))] - μ_0(X_i)
    }

donde:
    - e(X) es el propensity score
    - μ_t(X) = E[Y | T=t, X] son los outcome regressions

Propiedad clave (double robustness):
    Es consistente si AL MENOS UNO de e(X) o μ_t(X) está bien especificado.

Referencias:
    - Robins, Rotnitzky & Zhao (1994)
    - Glynn & Quinn (2010), "An Introduction to the Augmented IPW Estimator"
    - Hernán & Robins, "Causal Inference: What If", Ch.13
"""

from __future__ import annotations

import pandas as pd

from causal_pipeline.interfaces import ATEResult, CausalDAG


def estimate_ate_aipw(
    df: pd.DataFrame,
    dag: CausalDAG,
    treatment: str,
    outcome: str,
    n_bootstrap: int = 1000,
    propensity_model: str = "logistic",
    outcome_model: str = "random_forest",
    trim_threshold: float = 0.05,
    seed: int = 42,
) -> ATEResult:
    """Estimación AIPW del ATE.

    Pasos:
        1. Encontrar adjustment set via backdoor criterion.
        2. Fittear propensity score e(X).
        3. Fittear outcome regressions μ_0(X) y μ_1(X).
        4. Aplicar trimming si es necesario.
        5. Computar AIPW.
        6. Bootstrap para CI.

    Parameters
    ----------
    df : DataFrame.
    dag : DAG causal.
    treatment, outcome : nombres de columnas.
    n_bootstrap : muestras bootstrap.
    propensity_model : modelo para e(X) ("logistic" | "random_forest").
    outcome_model : modelo para μ_t(X) ("linear" | "random_forest").
    trim_threshold : umbral para trimming.
    seed : semilla.

    Returns
    -------
    ATEResult.
    """
    raise NotImplementedError("Persona B — implementar AIPW")
