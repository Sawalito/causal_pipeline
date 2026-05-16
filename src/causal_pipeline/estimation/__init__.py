"""Estimation — Persona B.

Identificación y estimación de efectos causales.
"""

import pandas as pd

from causal_pipeline.estimation.aipw import estimate_ate_aipw
from causal_pipeline.estimation.backdoor import find_backdoor_adjustment_set
from causal_pipeline.estimation.ipw import estimate_ate_ipw
from causal_pipeline.estimation.propensity import fit_propensity_score
from causal_pipeline.interfaces import ATEResult, CausalDAG


def estimate_ate(
    df: pd.DataFrame,
    dag: CausalDAG,
    treatment: str,
    outcome: str,
    method: str = "aipw",
    n_bootstrap: int = 1000,
    seed: int = 42,
) -> ATEResult:
    """Punto de entrada unificado para estimación de ATE.

    Esta firma DEBE coincidir con `interfaces.estimate_ate_signature`.
    """
    if method == "ipw":
        return estimate_ate_ipw(df, dag, treatment, outcome, n_bootstrap=n_bootstrap, seed=seed)
    if method == "aipw":
        return estimate_ate_aipw(df, dag, treatment, outcome, n_bootstrap=n_bootstrap, seed=seed)
    raise ValueError(f"Método desconocido: {method}")


__all__ = [
    "estimate_ate",
    "estimate_ate_aipw",
    "estimate_ate_ipw",
    "find_backdoor_adjustment_set",
    "fit_propensity_score",
]
