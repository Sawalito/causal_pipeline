"""Tests para el módulo de estimation (Persona B)."""

from __future__ import annotations

import networkx as nx
import pandas as pd
import pytest

from causal_pipeline.application.lalonde_dag_mock import (
    get_lalonde_dag_mock,
    get_minimal_backdoor_set,
)
from causal_pipeline.estimation import estimate_ate


@pytest.mark.skip(reason="Persona B: implementar backdoor criterion")
def test_backdoor_finds_minimal_set() -> None:
    """En el DAG de Lalonde, el conjunto backdoor mínimo debe contener todas las
    covariables predecesoras de treat y outcome."""
    from causal_pipeline.estimation.backdoor import find_backdoor_adjustment_set

    dag = get_lalonde_dag_mock()
    adj_set = find_backdoor_adjustment_set(dag, treatment="treat", outcome="re78", minimal=True)

    expected = set(get_minimal_backdoor_set())
    assert set(adj_set) == expected, f"Esperado {expected}, obtenido {set(adj_set)}"


@pytest.mark.skip(reason="Persona B: implementar IPW")
def test_ipw_recovers_known_ate(
    known_ate_data: tuple[pd.DataFrame, float],
    known_ate_dag: nx.DiGraph,
) -> None:
    """IPW debe converger al ATE verdadero (= 2.0) con n=5000."""
    df, true_ate = known_ate_data
    result = estimate_ate(df, known_ate_dag, "T", "Y", method="ipw", n_bootstrap=200)

    assert abs(result.point_estimate - true_ate) < 0.2, (
        f"IPW dio {result.point_estimate:.3f}, verdadero ATE es {true_ate}"
    )
    assert result.ci_low < true_ate < result.ci_high, (
        f"CI [{result.ci_low:.3f}, {result.ci_high:.3f}] no cubre el verdadero {true_ate}"
    )


@pytest.mark.skip(reason="Persona B: implementar AIPW")
def test_aipw_recovers_known_ate(
    known_ate_data: tuple[pd.DataFrame, float],
    known_ate_dag: nx.DiGraph,
) -> None:
    """AIPW debe ser al menos tan preciso como IPW."""
    df, true_ate = known_ate_data
    result = estimate_ate(df, known_ate_dag, "T", "Y", method="aipw", n_bootstrap=200)

    assert abs(result.point_estimate - true_ate) < 0.15
    assert result.ci_low < true_ate < result.ci_high


@pytest.mark.skip(reason="Persona B: implementar AIPW con doubly robustness")
@pytest.mark.slow
def test_aipw_is_doubly_robust(known_ate_data: tuple[pd.DataFrame, float]) -> None:
    """Si propensity está mal especificado pero outcome bien (o viceversa),
    AIPW sigue siendo consistente. Este test verifica esa propiedad."""
    raise NotImplementedError("Persona B — implementar test de double robustness")
