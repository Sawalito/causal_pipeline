# Reporte Final — Causal Pipeline aplicada a Lalonde

**Equipo:** Persona A, Persona B, Persona C
**Curso:** Foundations of AI
**Fecha de entrega:** 21 de mayo de 2026

---

## Resumen ejecutivo

*(Persona C — escribir al final, una vez todos los resultados estén listos)*

Tres oraciones que respondan: qué hicimos, qué encontramos, por qué importa.

---

## 1. Introducción y motivación

*(Persona C)*

- Distinción entre tres niveles de Pearl: asociación, intervención, contrafactual.
- Por qué los modelos predictivos puros no responden preguntas causales.
- Dataset Lalonde: contexto, importancia histórica, benchmark experimental.

---

## 2. Marco teórico

### 2.1 Structure learning con PC algorithm

*(Persona A)*

- Independencia condicional y faithfulness.
- Fase de skeleton: eliminación de aristas por tests CI.
- Fase de orientation: v-structures y reglas de Meek.

### 2.2 Identificación causal

*(Persona B)*

- DAGs y caminos backdoor.
- Backdoor criterion y conjunto de ajuste mínimo.

### 2.3 Estimación

*(Persona B)*

- Propensity score y unconfoundedness.
- IPW: Horvitz-Thompson y versión estabilizada.
- AIPW (doubly robust).

### 2.4 Contrafactuales

*(Persona C)*

- Structural Causal Models.
- Procedimiento de tres pasos: abducción, acción, predicción.

---

## 3. Metodología

### 3.1 Dataset Lalonde

*(Persona C)*

- N obs, N tratados, covariables, outcome.
- Benchmark experimental ATE ≈ $1,794.

### 3.2 DAG aprendido vs DAG de literatura

*(Persona A)*

- DAG mock de Dehejia & Wahba.
- DAG aprendido por PC con α=0.05.
- Comparación: aristas coincidentes, discrepancias, posibles causas.

### 3.3 Estimadores aplicados

*(Persona B)*

- IPW estabilizado.
- AIPW con outcome model = Random Forest.
- Bootstrap con B=1000.

---

## 4. Resultados

### 4.1 Recuperación del DAG sintético

*(Persona A)*

Tabla: % de aristas correctas en DAGs sintéticos de tamaño 5, 10, 15 nodos.

### 4.2 Estimación del ATE en Lalonde

*(Persona B)*

| Método | ATE | SE | CI 95% | Sesgo vs experimental |
|--------|-----|----|----|----------|
| Experimental (benchmark) | $1,794 | — | — | 0 |
| IPW | ? | ? | ? | ? |
| AIPW | ? | ? | ? | ? |
| OLS ajustado | ? | ? | ? | ? |
| RF baseline (pseudo-ATE) | ? | ? | ? | ? |

### 4.3 Query contrafactual de ejemplo

*(Persona C)*

Individuo tratado seleccionado: re78 observado = $X.
Contrafactual: si no hubiera recibido tratamiento, re78 estimado = $Y (CI: ...).

### 4.4 Demo de Simpson's paradox sintético

*(Persona C)*

Setup sintético, naive estimate, adjusted estimate, conclusión.

---

## 5. Discusión

### 5.1 ¿Recuperamos el benchmark experimental?

*(Persona B + C)*

Análisis de qué tan cerca quedó la estimación observacional del benchmark experimental.
Discusión de sources de discrepancia (selection on unobservables, mis-especificación, etc.).

### 5.2 ¿Por qué falla el baseline predictivo?

*(Persona C)*

Demostrar empíricamente la distinción P(Y|X) vs P(Y|do(X)).

### 5.3 Limitaciones

- Estabilidad de PC con muestra finita.
- Supuesto de unconfoundedness no testeable.
- Linealidad implícita de varios estimadores.

---

## 6. Conclusiones

*(Todos)*

Tres puntos clave para llevarse.

---

## Referencias

1. Pearl, J. (2009). *Causality*. Cambridge University Press.
2. Spirtes, P., Glymour, C., & Scheines, R. (2000). *Causation, Prediction, and Search*. MIT Press.
3. Dehejia, R., & Wahba, S. (1999). Causal effects in nonexperimental studies: Reevaluating the evaluation of training programs. *JASA*.
4. Glynn, A., & Quinn, K. (2010). An introduction to the augmented inverse propensity weighted estimator. *Political Analysis*.
5. Hernán, M., & Robins, J. (2020). *Causal Inference: What If*. CRC Press.

---

## Apéndice A: Reproducibilidad

```bash
git clone <repo-url>
cd causal_pipeline
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make test
make run --learned-dag
```
