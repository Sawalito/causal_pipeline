"""Fixtures compartidos para tests."""

from __future__ import annotations

import networkx as nx
import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="session")
def small_synthetic_dag() -> nx.DiGraph:
    """DAG sintético pequeño para validar structure learning."""
    dag = nx.DiGraph()
    dag.add_edges_from([("X1", "X3"), ("X2", "X3"), ("X3", "X4"), ("X2", "X4")])
    return dag


@pytest.fixture(scope="session")
def small_synthetic_data(small_synthetic_dag: nx.DiGraph) -> pd.DataFrame:
    """Datos generados desde un SCM lineal sobre el DAG sintético.

    SCM:
        X1 ~ N(0, 1)
        X2 ~ N(0, 1)
        X3 = 0.5 * X1 + 0.7 * X2 + N(0, 0.3)
        X4 = 0.8 * X3 + 0.4 * X2 + N(0, 0.3)
    """
    rng = np.random.default_rng(42)
    n = 1000
    x1 = rng.standard_normal(n)
    x2 = rng.standard_normal(n)
    x3 = 0.5 * x1 + 0.7 * x2 + rng.normal(0, 0.3, n)
    x4 = 0.8 * x3 + 0.4 * x2 + rng.normal(0, 0.3, n)
    return pd.DataFrame({"X1": x1, "X2": x2, "X3": x3, "X4": x4})


@pytest.fixture(scope="session")
def known_ate_data() -> tuple[pd.DataFrame, float]:
    """Dataset simulado con ATE conocido para validar estimadores.

    SCM:
        X ~ N(0, 1)
        T ~ Bernoulli(sigmoid(0.5 * X))
        Y = 2.0 * T + 1.5 * X + N(0, 0.5)

    ATE verdadero = 2.0
    """
    rng = np.random.default_rng(42)
    n = 5000
    x = rng.standard_normal(n)
    propensity = 1 / (1 + np.exp(-0.5 * x))
    t = rng.binomial(1, propensity)
    y = 2.0 * t + 1.5 * x + rng.normal(0, 0.5, n)
    df = pd.DataFrame({"X": x, "T": t, "Y": y})
    return df, 2.0


@pytest.fixture(scope="session")
def known_ate_dag() -> nx.DiGraph:
    """DAG para el dataset known_ate_data."""
    dag = nx.DiGraph()
    dag.add_edges_from([("X", "T"), ("X", "Y"), ("T", "Y")])
    return dag
