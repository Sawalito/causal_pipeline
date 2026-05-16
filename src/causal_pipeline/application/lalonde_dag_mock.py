"""DAG causal de Lalonde basado en literatura (Dehejia & Wahba, 1999).

Este es el DAG "ground truth" que el equipo asume mientras Persona A construye PC.
B y C lo usan desde el día 1 para no estar bloqueados.

El día 4, Persona A entrega el DAG aprendido y se reemplaza el uso del mock por
el aprendido en `application/lalonde_main.py`.
"""

from __future__ import annotations

import networkx as nx


def get_lalonde_dag_mock() -> nx.DiGraph:
    """Construye el DAG causal asumido para Lalonde según literatura.

    Estructura causal:
        - Demografía (age, educ, black, hispan, married, nodegree) afecta:
            * la probabilidad de recibir el tratamiento
            * los ingresos previos (re74, re75)
            * los ingresos finales (re78)
        - re74 → re75 (auto-regresión)
        - re74, re75 → treat (selección sobre ingresos previos)
        - re74, re75 → re78
        - treat → re78 (efecto causal de interés)

    Returns
    -------
    networkx.DiGraph con nodos = nombres de columnas de Lalonde.
    """
    dag = nx.DiGraph()

    demographics = ["age", "educ", "black", "hispan", "married", "nodegree"]
    prior_earnings = ["re74", "re75"]
    treatment = "treat"
    outcome = "re78"

    dag.add_nodes_from(demographics + prior_earnings + [treatment, outcome])

    # Demografía → tratamiento (selección)
    for d in demographics:
        dag.add_edge(d, treatment)

    # Demografía → ingresos previos
    for d in demographics:
        for e in prior_earnings:
            dag.add_edge(d, e)

    # Auto-regresión de ingresos
    dag.add_edge("re74", "re75")

    # Ingresos previos → tratamiento (selección sobre ingresos)
    for e in prior_earnings:
        dag.add_edge(e, treatment)

    # Demografía → outcome
    for d in demographics:
        dag.add_edge(d, outcome)

    # Ingresos previos → outcome
    for e in prior_earnings:
        dag.add_edge(e, outcome)

    # Efecto causal de interés
    dag.add_edge(treatment, outcome)

    assert nx.is_directed_acyclic_graph(dag), "El DAG mock contiene ciclos"
    return dag


def get_minimal_backdoor_set() -> list[str]:
    """Conjunto de ajuste backdoor mínimo válido según el DAG mock.

    Este conjunto bloquea todos los caminos backdoor entre `treat` y `re78`.
    Útil para que B compare contra esto al validar su implementación de backdoor.
    """
    return ["age", "educ", "black", "hispan", "married", "nodegree", "re74", "re75"]
