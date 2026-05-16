"""Structural Causal Model (SCM) fitting y sampling.

PERSONA C — Implementar.

Un SCM consiste en:
    - Un DAG G.
    - Para cada nodo V, una función estructural f_V(parents(V), U_V),
      donde U_V es ruido exógeno independiente.

Fitting:
    Para cada nodo V, ajustar una regresión:
        V = f_V(parents(V)) + U_V
    El residuo es una realización del ruido exógeno.

Sampling:
    1. Muestrear ruido exógeno U_V para cada nodo.
    2. Evaluar nodos en orden topológico.

Para contrafactuales necesitamos también:
    - Abducción: inferir el ruido latente que produjo la observación factual.
    - Esto se hace simplemente computando residuos en el SCM ajustado.

Referencias:
    - Pearl (2009), Causality, Ch.7
    - Peters, Janzing, Schölkopf (2017), Elements of Causal Inference, Ch.6-7
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from causal_pipeline.interfaces import CausalDAG


@dataclass
class StructuralCausalModel:
    """SCM ajustado, listo para sampleo e intervenciones.

    Attributes
    ----------
    dag : DAG estructural.
    models : dict de {nodo: modelo ajustado}.
    residual_distributions : dict de {nodo: empirical distribution of residuals}.
    topological_order : orden topológico para sampling.
    """

    dag: CausalDAG
    models: dict
    residual_distributions: dict
    topological_order: list[str]

    def predict(self, parents_values: dict, node: str) -> float:
        """Predicción puntual de un nodo dado los valores de sus padres."""
        raise NotImplementedError("Persona C — implementar predict")

    def sample(
        self,
        intervention: dict | None = None,
        noise_seed: int | None = None,
        n: int = 1,
    ) -> pd.DataFrame:
        """Samplea del SCM, opcionalmente bajo intervención do(V=v).

        Parameters
        ----------
        intervention : dict {variable: valor fijo}. Si None, sample observacional.
        noise_seed : semilla para el ruido.
        n : número de muestras.

        Returns
        -------
        DataFrame con n filas y una columna por nodo.
        """
        raise NotImplementedError("Persona C — implementar sampling con intervención")

    def abduct_noise(self, observation: dict) -> dict:
        """Paso de abducción: dado una observación factual, recuperar el ruido latente.

        Para cada nodo, calcular U_V = V - f_V(parents(V)).

        Returns
        -------
        dict {nodo: valor del ruido}.
        """
        raise NotImplementedError("Persona C — implementar abducción")


def fit_scm(
    df: pd.DataFrame,
    dag: CausalDAG,
    model_type: str = "linear",
    seed: int = 42,
) -> StructuralCausalModel:
    """Ajusta un SCM al DAG y los datos.

    Para cada nodo del DAG en orden topológico, ajusta una regresión:
        nodo ~ parents(nodo)

    Parameters
    ----------
    df : DataFrame.
    dag : DAG estructural.
    model_type : "linear" | "random_forest" | "gradient_boosting".
    seed : semilla.

    Returns
    -------
    StructuralCausalModel ajustado.
    """
    raise NotImplementedError("Persona C — implementar fit_scm")
