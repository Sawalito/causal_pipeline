"""GES (Greedy Equivalence Search) — algoritmo basado en score.

OPCIONAL — Persona A puede implementarlo como baseline alternativo a PC.

Idea:
    Búsqueda greedy en el espacio de equivalencia de Markov, optimizando BIC.
    Dos fases:
        - Forward: agregar aristas mientras mejore el score.
        - Backward: eliminar aristas mientras mejore el score.

Referencia:
    - Chickering (2002), "Optimal Structure Identification with Greedy Search"
"""

from __future__ import annotations

import pandas as pd

from causal_pipeline.interfaces import CausalDAG


def ges_algorithm(df: pd.DataFrame, seed: int = 42) -> CausalDAG:
    """GES algorithm para structure learning."""
    raise NotImplementedError("Persona A — opcional: implementar GES")
