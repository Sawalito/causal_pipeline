"""Backdoor criterion para identificación de efectos causales.

PERSONA B — Implementar.

Idea:
    Dado un DAG, treatment T y outcome Y, encontrar un conjunto Z de variables
    tal que:
        a. Z bloquea todos los caminos backdoor entre T e Y.
        b. Z no contiene descendientes de T.

    Si tal Z existe, el efecto causal P(Y | do(T)) es identificable como:
        P(Y | do(T=t)) = Σ_z P(Y | T=t, Z=z) P(Z=z)

Referencias:
    - Pearl (2009), Causality, Ch.3
    - Shpitser, VanderWeele & Robins (2010), "On the validity of covariate adjustment"
"""

from __future__ import annotations

import networkx as nx

from causal_pipeline.interfaces import CausalDAG


def find_backdoor_adjustment_set(
    dag: CausalDAG,
    treatment: str,
    outcome: str,
    minimal: bool = True,
) -> list[str]:
    """Encuentra un conjunto de ajuste backdoor válido.

    Parameters
    ----------
    dag : DAG causal.
    treatment, outcome : nombres de variables.
    minimal : si True, retornar conjunto mínimo. Si False, retornar el conjunto
              de todos los no-descendientes que son padres de T o Y.

    Returns
    -------
    Lista de nombres de variables a controlar.

    Raises
    ------
    ValueError si no existe un conjunto backdoor válido (no identificable).
    """
    raise NotImplementedError("Persona B — implementar backdoor criterion")


def get_backdoor_paths(dag: CausalDAG, treatment: str, outcome: str) -> list[list[str]]:
    """Enumera todos los caminos backdoor entre treatment y outcome.

    Útil para debugging y para diagnosticar si el conjunto de ajuste los bloquea.
    """
    raise NotImplementedError("Persona B — implementar enumeración de backdoor paths")


def is_valid_adjustment_set(
    dag: CausalDAG,
    treatment: str,
    outcome: str,
    adjustment_set: list[str],
) -> bool:
    """Verifica si un conjunto dado es un adjustment set válido."""
    raise NotImplementedError("Persona B — implementar verificación de adjustment set")
