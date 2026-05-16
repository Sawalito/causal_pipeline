"""Pipeline end-to-end sobre Lalonde.

PERSONA C — Mantener y orquestar este archivo.

Día 1-3: usa DAG mock para que el pipeline corra sin depender de Persona A.
Día 4+: reemplaza DAG mock por DAG aprendido por PC.

Ejecutar:
    make run
    # o:
    python -m causal_pipeline.application.lalonde_main

Outputs esperados:
    - ATE estimado con CI (IPW, AIPW)
    - Comparación con benchmark experimental ($1,794)
    - Comparación con baseline predictivo (RF)
    - Query contrafactual de ejemplo
"""

from __future__ import annotations

import logging
import sys

from causal_pipeline.application.lalonde_dag_mock import get_lalonde_dag_mock
from causal_pipeline.baselines import random_forest_baseline
from causal_pipeline.counterfactuals import counterfactual_query
from causal_pipeline.estimation import estimate_ate
from causal_pipeline.structure_learning import learn_structure
from causal_pipeline.utils import (
    COVARIATES,
    OUTCOME_COL,
    TREATMENT_COL,
    load_lalonde,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

EXPERIMENTAL_BENCHMARK_ATE = 1794.0
SEED = 42


def run_pipeline(use_learned_dag: bool = False) -> dict:
    """Ejecuta la pipeline completa.

    Parameters
    ----------
    use_learned_dag : si True, usa el DAG aprendido por PC.
                      Si False (default días 1-3), usa el DAG mock de literatura.

    Returns
    -------
    dict con todos los resultados.
    """
    results: dict = {}

    # ------------------------------------------------------------------
    # Paso 0: cargar datos
    # ------------------------------------------------------------------
    logger.info("Cargando dataset Lalonde...")
    df = load_lalonde()
    logger.info(f"Dataset cargado: {len(df)} observaciones, {df[TREATMENT_COL].sum()} tratados")
    results["n_obs"] = len(df)
    results["n_treated"] = int(df[TREATMENT_COL].sum())

    # ------------------------------------------------------------------
    # Paso 1: obtener DAG (mock o aprendido)
    # ------------------------------------------------------------------
    if use_learned_dag:
        logger.info("Aprendiendo DAG con PC algorithm...")
        dag = learn_structure(df, method="pc", alpha=0.05, seed=SEED)
        results["dag_source"] = "learned (PC)"
    else:
        logger.info("Usando DAG mock de literatura (Dehejia & Wahba 1999)...")
        dag = get_lalonde_dag_mock()
        results["dag_source"] = "literature mock"

    results["dag_n_edges"] = dag.number_of_edges()

    # ------------------------------------------------------------------
    # Paso 2: estimar ATE con múltiples métodos
    # ------------------------------------------------------------------
    logger.info("Estimando ATE con IPW...")
    ate_ipw = estimate_ate(df, dag, TREATMENT_COL, OUTCOME_COL, method="ipw", seed=SEED)
    results["ate_ipw"] = ate_ipw

    logger.info("Estimando ATE con AIPW (doubly robust)...")
    ate_aipw = estimate_ate(df, dag, TREATMENT_COL, OUTCOME_COL, method="aipw", seed=SEED)
    results["ate_aipw"] = ate_aipw

    # ------------------------------------------------------------------
    # Paso 3: baseline predictivo (Random Forest)
    # ------------------------------------------------------------------
    logger.info("Calculando baseline predictivo (Random Forest)...")
    rf_baseline = random_forest_baseline(
        df, TREATMENT_COL, OUTCOME_COL, COVARIATES, seed=SEED,
    )
    results["rf_baseline"] = rf_baseline

    # ------------------------------------------------------------------
    # Paso 4: query contrafactual de ejemplo
    # ------------------------------------------------------------------
    logger.info("Computando query contrafactual de ejemplo...")
    # Tomar un individuo tratado: ¿cuánto habría ganado sin tratamiento?
    treated_individual = df[df[TREATMENT_COL] == 1].iloc[0].to_dict()
    cf_result = counterfactual_query(
        df=df,
        dag=dag,
        factual=treated_individual,
        intervention={TREATMENT_COL: 0},
        target=OUTCOME_COL,
        seed=SEED,
    )
    results["counterfactual_example"] = {
        "factual_outcome": treated_individual[OUTCOME_COL],
        "counterfactual": cf_result,
    }

    # ------------------------------------------------------------------
    # Paso 5: reporte de resultados
    # ------------------------------------------------------------------
    _print_summary(results)
    return results


def _print_summary(results: dict) -> None:
    """Imprime un resumen legible de los resultados."""
    print("\n" + "=" * 70)
    print("RESUMEN — Causal Pipeline sobre Lalonde")
    print("=" * 70)
    print(f"Observaciones: {results['n_obs']}")
    print(f"Tratados: {results['n_treated']}")
    print(f"DAG: {results['dag_source']} ({results['dag_n_edges']} aristas)")
    print()
    print(f"Benchmark experimental:  ATE = ${EXPERIMENTAL_BENCHMARK_ATE:,.2f}")
    print(f"IPW:                     {results['ate_ipw']}")
    print(f"AIPW (doubly robust):    {results['ate_aipw']}")
    print(f"RF baseline (sesgado):   pseudo-ATE = ${results['rf_baseline'].pseudo_ate:,.2f}")
    print()
    print(f"Contrafactual ejemplo: {results['counterfactual_example']['counterfactual']}")
    print("=" * 70)


def main() -> None:
    """Entry point para `python -m causal_pipeline.application.lalonde_main`."""
    import argparse

    parser = argparse.ArgumentParser(description="Run causal pipeline on Lalonde dataset")
    parser.add_argument(
        "--learned-dag",
        action="store_true",
        help="Usar DAG aprendido por PC (default: DAG mock de literatura)",
    )
    args = parser.parse_args()

    run_pipeline(use_learned_dag=args.learned_dag)


if __name__ == "__main__":
    main()
