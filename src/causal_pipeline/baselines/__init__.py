"""Baselines — Persona C.

Modelos puramente predictivos para contraste con métodos causales.
"""

from causal_pipeline.baselines.predictive import (
    PredictiveBaselineResult,
    random_forest_baseline,
    simpsons_paradox_demo,
)

__all__ = ["PredictiveBaselineResult", "random_forest_baseline", "simpsons_paradox_demo"]
