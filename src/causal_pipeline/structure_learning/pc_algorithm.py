"""PC Algorithm para structure learning.

PERSONA A — Implementar las dos fases:
    1. Skeleton phase: construir grafo no dirigido eliminando aristas
       cuando se encuentra independencia condicional.
    2. Orientation phase: orientar aristas vía v-structures y reglas de Meek.

Referencias:
    - Spirtes, Glymour, Scheines (2000), Causation, Prediction, and Search, Ch.5
    - Pearl (2009), Causality, Ch.2
    - Meek (1995), "Causal inference and causal explanation with background knowledge"

Validación:
    - DAGs sintéticos pequeños con datos generados por SCM lineal.
    - Comparar contra `causal-learn` como benchmark externo.
"""

from __future__ import annotations

import networkx as nx
import pandas as pd

from causal_pipeline.interfaces import CausalDAG


def learn_structure(
    df: pd.DataFrame,
    method: str = "pc",
    alpha: float = 0.05,
    seed: int = 42,
) -> CausalDAG:
    """Aprende un DAG causal desde datos observacionales.

    PUNTO DE ENTRADA público del módulo de structure learning.
    Esta firma DEBE coincidir con `interfaces.learn_structure_signature`.
    """
    if method == "pc":
        return _pc_algorithm(df, alpha=alpha, seed=seed)
    if method == "ges":
        from causal_pipeline.structure_learning.ges import ges_algorithm
        return ges_algorithm(df, seed=seed)
    raise ValueError(f"Método desconocido: {method}")


def _pc_algorithm(df: pd.DataFrame, alpha: float, seed: int) -> CausalDAG:
    """PC algorithm en dos fases.

    PERSONA A — implementar.
    """
    skeleton, separating_sets = _build_skeleton(df, alpha)
    dag = _orient_edges(skeleton, separating_sets)
    return dag


def _build_skeleton(
    df: pd.DataFrame,
    alpha: float,
) -> tuple[nx.Graph, dict[tuple[str, str], list[str]]]:
    """Fase 1: skeleton.

    Parte de un grafo completo y elimina aristas según tests CI.
    Aumenta progresivamente el tamaño del conditioning set.

    Returns
    -------
    skeleton : grafo no dirigido.
    separating_sets : {(x, y): conjunto separador encontrado}.
    """
    raise NotImplementedError("Persona A — implementar skeleton phase")


def _orient_edges(
    skeleton: nx.Graph,
    separating_sets: dict[tuple[str, str], list[str]],
) -> CausalDAG:
    """Fase 2: orientation.

    Pasos:
        a. Identificar v-structures (X → Z ← Y donde X-Z, Z-Y, X⊥Y).
        b. Aplicar reglas de Meek (R1-R4) para orientar aristas adicionales.
        c. Las aristas que queden sin orientar se devuelven como bidireccionales
           o se orientan arbitrariamente (documentar la decisión).
    """
    raise NotImplementedError("Persona A — implementar orientation phase")
