"""Counterfactuals — Persona C.

SCM fitting y razonamiento contrafactual.
"""

from causal_pipeline.counterfactuals.scm import StructuralCausalModel, fit_scm
from causal_pipeline.counterfactuals.three_step import counterfactual_query

__all__ = ["StructuralCausalModel", "counterfactual_query", "fit_scm"]
