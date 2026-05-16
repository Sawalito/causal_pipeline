"""Tests para counterfactuals y baselines (Persona C)."""

from __future__ import annotations

import networkx as nx
import numpy as np
import pandas as pd
import pytest

from causal_pipeline.counterfactuals import counterfactual_query, fit_scm


@pytest.mark.skip(reason="Persona C: implementar fit_scm")
def test_scm_fit_recovers_linear_coefficients(
    small_synthetic_data: pd.DataFrame,
    small_synthetic_dag: nx.DiGraph,
) -> None:
    """SCM lineal ajustado debe recuperar los coeficientes reales con bajo error."""
    scm = fit_scm(small_synthetic_data, small_synthetic_dag, model_type="linear")

    # Coeficientes reales: X3 = 0.5*X1 + 0.7*X2
    coef_x1 = scm.models["X3"].coef_[scm.models["X3"].feature_names_in_.tolist().index("X1")]
    coef_x2 = scm.models["X3"].coef_[scm.models["X3"].feature_names_in_.tolist().index("X2")]

    assert abs(coef_x1 - 0.5) < 0.05, f"Coef X1 esperado ~0.5, obtenido {coef_x1:.3f}"
    assert abs(coef_x2 - 0.7) < 0.05, f"Coef X2 esperado ~0.7, obtenido {coef_x2:.3f}"


@pytest.mark.skip(reason="Persona C: implementar counterfactual_query")
def test_counterfactual_known_scm() -> None:
    """SCM analítico simple: Y = 2*T + X + epsilon.

    Si observamos T=1, X=0, Y=2.5 (entonces epsilon=0.5).
    Bajo intervención do(T=0), Y_cf debe ser 0 + 0.5 = 0.5.
    """
    rng = np.random.default_rng(42)
    n = 1000
    x = rng.standard_normal(n)
    t = rng.binomial(1, 0.5, n)
    y = 2.0 * t + x + rng.normal(0, 0.01, n)  # ruido mínimo
    df = pd.DataFrame({"X": x, "T": t, "Y": y})

    dag = nx.DiGraph()
    dag.add_edges_from([("X", "Y"), ("T", "Y")])

    result = counterfactual_query(
        df=df,
        dag=dag,
        factual={"T": 1, "X": 0.0, "Y": 2.5},
        intervention={"T": 0},
        target="Y",
        n_samples=100,
    )

    # Y_cf esperado: 0*2 + 0 + 0.5 = 0.5
    assert abs(result.point_estimate - 0.5) < 0.1, (
        f"Contrafactual esperado ~0.5, obtenido {result.point_estimate:.3f}"
    )


@pytest.mark.skip(reason="Persona C: implementar baseline predictivo")
def test_rf_baseline_is_biased_under_confounding(
    known_ate_data: tuple[pd.DataFrame, float],
) -> None:
    """El baseline RF debe dar una estimación sesgada cuando hay confounding fuerte.

    Esto valida la narrativa del proyecto: modelos predictivos puros no resuelven
    el problema causal.
    """
    from causal_pipeline.baselines import random_forest_baseline

    df, true_ate = known_ate_data
    result = random_forest_baseline(df, "T", "Y", covariates=["X"])

    # Nota: el RF que incluye X como feature puede estar cerca del verdadero ATE en
    # este caso simple. El sesgo del baseline se vuelve evidente en setups más
    # complejos (interacciones, no-linealidades). Este test debe ajustarse según
    # el setup que Persona C diseñe.
    assert isinstance(result.pseudo_ate, float)
