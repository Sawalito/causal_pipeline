"""Visualización de DAGs causales."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx


def plot_dag(
    dag: nx.DiGraph,
    title: str = "Causal DAG",
    highlight_path: list[tuple[str, str]] | None = None,
    ax: plt.Axes | None = None,
    layout: str = "spring",
    seed: int = 42,
) -> plt.Axes:
    """Renderiza un DAG con opción de resaltar un camino causal.

    Parameters
    ----------
    dag : DAG a visualizar.
    title : título del plot.
    highlight_path : lista de aristas (u, v) a destacar (e.g., camino causal de T a Y).
    ax : ejes matplotlib opcionales.
    layout : "spring", "circular", "kamada_kawai".
    seed : semilla para layouts estocásticos.

    Returns
    -------
    Ejes de matplotlib.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 7))

    if layout == "spring":
        pos = nx.spring_layout(dag, seed=seed)
    elif layout == "circular":
        pos = nx.circular_layout(dag)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(dag)
    else:
        raise ValueError(f"Layout desconocido: {layout}")

    edge_colors = []
    edge_widths = []
    for u, v in dag.edges():
        if highlight_path and (u, v) in highlight_path:
            edge_colors.append("crimson")
            edge_widths.append(2.5)
        else:
            edge_colors.append("gray")
            edge_widths.append(1.0)

    nx.draw_networkx_nodes(dag, pos, node_color="lightblue", node_size=2000, ax=ax)
    nx.draw_networkx_labels(dag, pos, font_size=10, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(
        dag, pos,
        edge_color=edge_colors,
        width=edge_widths,
        arrowsize=20,
        arrowstyle="->",
        ax=ax,
    )

    ax.set_title(title, fontsize=14)
    ax.axis("off")
    return ax


def compare_dags(
    dag_true: nx.DiGraph,
    dag_learned: nx.DiGraph,
    title_true: str = "True DAG (literature)",
    title_learned: str = "Learned DAG (PC)",
) -> plt.Figure:
    """Compara visualmente dos DAGs lado a lado."""
    fig, axes = plt.subplots(1, 2, figsize=(20, 7))
    plot_dag(dag_true, title=title_true, ax=axes[0])
    plot_dag(dag_learned, title=title_learned, ax=axes[1])
    plt.tight_layout()
    return fig
