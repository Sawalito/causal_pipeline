"""Tests para el módulo de structure learning (Persona A)."""

from __future__ import annotations

import networkx as nx
import pandas as pd
import pytest

from causal_pipeline.structure_learning import learn_structure


@pytest.mark.skip(reason="Persona A: implementar Fisher Z primero")
def test_fisher_z_independent_variables(small_synthetic_data: pd.DataFrame) -> None:
    """Variables independientes deben NO rechazar H0 de independencia."""
    from causal_pipeline.structure_learning.ci_tests import fisher_z_test

    independent, p_value = fisher_z_test(small_synthetic_data, "X1", "X2")
    assert independent, f"X1 y X2 son independientes pero el test rechazó (p={p_value:.4f})"


@pytest.mark.skip(reason="Persona A: implementar Fisher Z primero")
def test_fisher_z_dependent_variables(small_synthetic_data: pd.DataFrame) -> None:
    """Variables dependientes (X1 → X3) deben rechazar H0."""
    from causal_pipeline.structure_learning.ci_tests import fisher_z_test

    independent, p_value = fisher_z_test(small_synthetic_data, "X1", "X3")
    assert not independent, f"X1 y X3 son dependientes pero el test no rechazó (p={p_value:.4f})"


@pytest.mark.skip(reason="Persona A: implementar PC algorithm")
def test_pc_recovers_synthetic_dag(
    small_synthetic_data: pd.DataFrame,
    small_synthetic_dag: nx.DiGraph,
) -> None:
    """PC algorithm debe recuperar la estructura del DAG sintético (al menos el skeleton)."""
    learned = learn_structure(small_synthetic_data, method="pc", alpha=0.05)

    # El skeleton debe coincidir (ignorando dirección)
    true_skeleton = set(map(frozenset, small_synthetic_dag.edges()))
    learned_skeleton = set(map(frozenset, learned.edges()))

    assert true_skeleton == learned_skeleton, (
        f"Skeleton incorrecto.\nEsperado: {true_skeleton}\nObtenido: {learned_skeleton}"
    )


@pytest.mark.skip(reason="Persona A: implementar PC algorithm con v-structures")
def test_pc_finds_v_structure(
    small_synthetic_data: pd.DataFrame,
) -> None:
    """X1 → X3 ← X2 es una v-structure. PC debe orientarla correctamente."""
    learned = learn_structure(small_synthetic_data, method="pc", alpha=0.05)

    assert learned.has_edge("X1", "X3"), "Arista X1 → X3 no orientada"
    assert learned.has_edge("X2", "X3"), "Arista X2 → X3 no orientada"
