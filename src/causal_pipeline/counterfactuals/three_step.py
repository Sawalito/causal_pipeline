"""Procedimiento de tres pasos para queries contrafactuales.

PERSONA C — Implementar.

Procedimiento (Pearl, 2009):
    1. ABDUCCIÓN: dado la observación factual, recuperar el ruido latente U.
    2. ACCIÓN: modificar el SCM con la intervención hipotética do(X = x').
    3. PREDICCIÓN: evaluar el SCM modificado con el ruido recuperado para
       obtener la variable objetivo en el mundo contrafactual.

Ejemplo:
    Factual:    Juan recibió tratamiento (T=1) y ganó re78=$10,000.
    Pregunta:   ¿Cuánto habría ganado Juan si NO hubiera recibido el tratamiento?
    Resultado:  P(re78_{T=0} | T=1, re78=$10,000, X=Juan)

Esto NO es lo mismo que el ATE:
    - ATE responde la pregunta poblacional E[Y_1 - Y_0].
    - Contrafactual responde una pregunta individual o de subgrupo.

Referencias:
    - Pearl (2009), Causality, Ch.7
    - Pearl, Glymour, Jewell (2016), Ch.4
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from causal_pipeline.counterfactuals.scm import StructuralCausalModel, fit_scm
from causal_pipeline.interfaces import CausalDAG, CounterfactualResult


def counterfactual_query(
    df: pd.DataFrame,
    dag: CausalDAG,
    factual: dict,
    intervention: dict,
    target: str,
    n_samples: int = 1000,
    seed: int = 42,
) -> CounterfactualResult:
    """Responde una query contrafactual sobre un individuo o subgrupo.

    Esta firma DEBE coincidir con `interfaces.counterfactual_query_signature`.

    Parameters
    ----------
    df : DataFrame para ajustar el SCM.
    dag : DAG estructural.
    factual : observación factual {variable: valor}.
    intervention : intervención hipotética {variable: valor}.
    target : variable de interés contrafactual.
    n_samples : muestras del SCM para construir la distribución.
    seed : semilla.

    Returns
    -------
    CounterfactualResult.
    """
    raise NotImplementedError("Persona C — implementar three-step procedure")


def _three_step(
    scm: StructuralCausalModel,
    factual: dict,
    intervention: dict,
    target: str,
    n_samples: int,
    seed: int,
) -> np.ndarray:
    """Ejecuta los tres pasos sobre un SCM ya ajustado.

    Returns
    -------
    Array de muestras contrafactuales de la variable target.
    """
    raise NotImplementedError("Persona C — implementar three-step procedure")
