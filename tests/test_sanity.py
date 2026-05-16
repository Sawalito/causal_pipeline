"""Sanity checks del scaffold. DEBEN PASAR desde el día 1.

Si alguno falla, el repo no está listo para que el equipo empiece a trabajar.
"""

from __future__ import annotations

import networkx as nx
import pandas as pd

from causal_pipeline.application.lalonde_dag_mock import (
    get_lalonde_dag_mock,
    get_minimal_backdoor_set,
)
from causal_pipeline.interfaces import ATEResult, CounterfactualResult


def test_imports() -> None:
    """Todos los módulos principales importan sin errores."""
    from causal_pipeline import counterfactuals, estimation, structure_learning, utils  # noqa: F401


def test_lalonde_dag_mock_is_dag() -> None:
    """El DAG mock de Lalonde es un DAG válido."""
    dag = get_lalonde_dag_mock()
    assert isinstance(dag, nx.DiGraph)
    assert nx.is_directed_acyclic_graph(dag)


def test_lalonde_dag_mock_has_expected_nodes() -> None:
    """El DAG mock contiene todos los nodos esperados de Lalonde."""
    dag = get_lalonde_dag_mock()
    expected_nodes = {
        "age", "educ", "black", "hispan", "married", "nodegree",
        "re74", "re75", "treat", "re78",
    }
    assert set(dag.nodes()) == expected_nodes


def test_lalonde_dag_mock_has_treatment_effect_edge() -> None:
    """treat → re78 debe ser una arista del DAG (el efecto causal de interés)."""
    dag = get_lalonde_dag_mock()
    assert dag.has_edge("treat", "re78")


def test_minimal_backdoor_set_is_consistent() -> None:
    """El backdoor mínimo debe ser un subconjunto de los nodos del DAG."""
    dag = get_lalonde_dag_mock()
    backdoor = get_minimal_backdoor_set()
    assert set(backdoor).issubset(set(dag.nodes()))


def test_ate_result_dataclass() -> None:
    """ATEResult se puede instanciar correctamente."""
    result = ATEResult(
        point_estimate=1800.0,
        std_error=200.0,
        ci_low=1400.0,
        ci_high=2200.0,
        adjustment_set=["age", "educ"],
        n_effective=500,
        method="aipw",
    )
    assert result.point_estimate == 1800.0
    assert "ATE" in repr(result)


def test_counterfactual_result_dataclass() -> None:
    """CounterfactualResult se puede instanciar correctamente."""
    import numpy as np
    result = CounterfactualResult(
        point_estimate=5000.0,
        distribution_samples=np.array([4800.0, 5100.0, 5050.0]),
        ci_low=4500.0,
        ci_high=5500.0,
        factual={"T": 1, "Y": 6000.0},
        intervention={"T": 0},
    )
    assert result.point_estimate == 5000.0
