"""
Interfaces compartidas entre módulos.

CRÍTICO: estas firmas son el contrato entre Personas A, B y C.
No modificar sin discusión grupal en daily standup.

Cualquier cambio aquí rompe la integración del día 4.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import networkx as nx
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

CausalDAG = nx.DiGraph
"""DAG causal. Nodos son nombres de columnas del DataFrame. Aristas son arrows causales."""

StructureMethod = Literal["pc", "ges"]
"""Algoritmos disponibles para structure learning."""

EstimationMethod = Literal["ipw", "aipw", "matching", "ols"]
"""Métodos disponibles para estimación de ATE."""


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ATEResult:
    """Resultado de la estimación de Average Treatment Effect.

    Esta es la salida estandarizada de TODOS los estimadores en el módulo `estimation`.
    """

    point_estimate: float
    std_error: float
    ci_low: float
    ci_high: float
    adjustment_set: list[str]
    n_effective: int
    method: EstimationMethod

    def __repr__(self) -> str:
        return (
            f"ATE = {self.point_estimate:.2f} "
            f"(SE = {self.std_error:.2f}, "
            f"95% CI = [{self.ci_low:.2f}, {self.ci_high:.2f}], "
            f"method = {self.method})"
        )


@dataclass
class CounterfactualResult:
    """Resultado de un query contrafactual.

    Salida estandarizada de `counterfactual_query` en el módulo `counterfactuals`.
    """

    point_estimate: float
    distribution_samples: np.ndarray
    ci_low: float
    ci_high: float
    factual: dict
    intervention: dict

    def __repr__(self) -> str:
        return (
            f"Counterfactual estimate = {self.point_estimate:.2f} "
            f"(95% CI = [{self.ci_low:.2f}, {self.ci_high:.2f}])"
        )


# ---------------------------------------------------------------------------
# Function signatures (contract)
# ---------------------------------------------------------------------------
# Estas son las firmas que cada módulo debe respetar.
# La implementación va en sus respectivos archivos.

def learn_structure_signature(
    df: pd.DataFrame,
    method: StructureMethod = "pc",
    alpha: float = 0.05,
    seed: int = 42,
) -> CausalDAG:
    """Aprende el DAG causal desde datos observacionales.

    Implementación en: src/causal_pipeline/structure_learning/pc_algorithm.py

    Parameters
    ----------
    df : DataFrame con las variables observadas. Columnas = nombres de variables.
    method : algoritmo a usar.
    alpha : nivel de significancia para tests de independencia condicional.
    seed : semilla para reproducibilidad.

    Returns
    -------
    DAG donde nodos son nombres de columnas de df.
    """
    raise NotImplementedError


def estimate_ate_signature(
    df: pd.DataFrame,
    dag: CausalDAG,
    treatment: str,
    outcome: str,
    method: EstimationMethod = "aipw",
    n_bootstrap: int = 1000,
    seed: int = 42,
) -> ATEResult:
    """Estima el efecto causal promedio del tratamiento sobre el outcome.

    Implementación en: src/causal_pipeline/estimation/{ipw,aipw}.py

    Parameters
    ----------
    df : DataFrame con todas las variables relevantes.
    dag : DAG causal (puede ser aprendido o mock).
    treatment : nombre de la columna del tratamiento (binario 0/1).
    outcome : nombre de la columna del outcome (continuo).
    method : método de estimación.
    n_bootstrap : número de muestras bootstrap para intervalos de confianza.
    seed : semilla para reproducibilidad.

    Returns
    -------
    ATEResult con estimación puntual, SE, CI y metadatos.
    """
    raise NotImplementedError


def counterfactual_query_signature(
    df: pd.DataFrame,
    dag: CausalDAG,
    factual: dict,
    intervention: dict,
    target: str,
    n_samples: int = 1000,
    seed: int = 42,
) -> CounterfactualResult:
    """Responde una query contrafactual sobre un individuo o subgrupo.

    Implementación en: src/causal_pipeline/counterfactuals/three_step.py

    Parameters
    ----------
    df : DataFrame para fittear el SCM.
    dag : DAG causal.
    factual : observación factual, dict {variable: valor}.
    intervention : intervención hipotética, dict {variable: valor}.
    target : nombre de la variable de interés contrafactual.
    n_samples : número de muestras del SCM para la distribución contrafactual.
    seed : semilla.

    Returns
    -------
    CounterfactualResult con estimación puntual y distribución.
    """
    raise NotImplementedError
