# Causal Pipeline — Proyecto Final IA

Pipeline end-to-end de inferencia causal aplicada al dataset Lalonde.
Aprende el DAG causal, identifica efectos intervencionales, estima ATE y responde queries contrafactuales.

**Entrega:** 21 de mayo de 2026
**Equipo:** 3 personas (A: Structure Learning, B: Estimation, C: Counterfactuals & Application)

---

## Quick Start

```bash
# 1. Clonar
git clone <repo-url> && cd causal_pipeline

# 2. Crear entorno (Python 3.11+)
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate

# 3. Instalar
pip install -e ".[dev]"

# 4. Verificar
make test

# 5. Ejecutar pipeline completa
make run
```

---

## Estructura

```
causal_pipeline/
├── src/causal_pipeline/
│   ├── interfaces.py              # CONTRATO entre módulos (no modificar sin acordar)
│   ├── structure_learning/        # Persona A
│   ├── estimation/                # Persona B
│   ├── counterfactuals/           # Persona C
│   ├── baselines/                 # Persona C (RF baseline)
│   ├── application/               # Pipeline end-to-end + DAG mock de Lalonde
│   └── utils/                     # Compartido (data loading, viz)
├── tests/                         # Tests pytest por módulo
├── notebooks/                     # Validación, EDA, resultados finales
├── data/                          # Dataset Lalonde
├── reports/                       # Reporte final
├── pyproject.toml
├── Makefile
└── README.md
```

---

## División del trabajo

| Persona | Módulo principal | Archivos a implementar |
|---------|------------------|------------------------|
| A | `structure_learning/` | `ci_tests.py`, `pc_algorithm.py`, `ges.py` |
| B | `estimation/` | `backdoor.py`, `propensity.py`, `ipw.py`, `aipw.py` |
| C | `counterfactuals/`, `baselines/`, `application/` | `scm.py`, `three_step.py`, `predictive.py`, `lalonde_main.py` |

Las interfaces entre módulos están en `src/causal_pipeline/interfaces.py`.
**No modificar sin discusión grupal.**

---

## Comandos disponibles

```bash
make install      # Instala el paquete en modo editable con deps de dev
make test         # Corre pytest
make lint         # Verifica formato y linting
make format       # Aplica black y ruff fix
make run          # Ejecuta el pipeline end-to-end sobre Lalonde
make clean        # Limpia caches y artefactos
```

---

## Checkpoints diarios

| Día | Fecha | Hito principal |
|-----|-------|----------------|
| 1 | Vie 15 | Setup, interfaces congeladas, datos cargados, DAG mock disponible |
| 2 | Sáb 16 | Prototipos por módulo con DAG mock |
| 3 | Dom 17 | Core de cada módulo + validación sintética |
| 4 | Lun 18 | Integración con DAG aprendido (CRÍTICO) |
| 5 | Mar 19 | Experimentos y robustez |
| 6 | Mié 20 | Reporte y demo |
| 7 | Jue 21 | Buffer y entrega |

Daily standup de 15 minutos cada día. Cada persona dice: qué hizo, qué hará, qué le bloquea.

---

## Validación

- **Persona A:** DAGs sintéticos con estructura conocida deben recuperarse correctamente (`tests/test_structure_learning.py`).
- **Persona B:** Datos simulados con ATE conocido deben converger (`tests/test_estimation.py`).
- **Persona C:** SCM sintético con respuesta contrafactual analítica (`tests/test_counterfactuals.py`).
- **Pipeline completo:** comparar ATE estimado vs benchmark experimental de Lalonde (~$1,794).

---

## Recursos clave

- Pearl, Glymour, Jewell (2016) — *Causal Inference in Statistics: A Primer*
- Hernán & Robins (2020) — *Causal Inference: What If* (gratis online)
- Peters, Janzing, Schölkopf (2017) — *Elements of Causal Inference*
- Dehejia & Wahba (1999) — análisis observacional de Lalonde

Ver `reports/final_report_skeleton.md` para la estructura del reporte final.
# causal_pipeline
