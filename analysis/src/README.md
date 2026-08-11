<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# analysis/src/ — Importable analysis package

## What belongs here

- Modules: `isotherms.py`, `kinetics.py`, `thermo.py`, `selectivity.py`, `column.py`, `speciation.py`, `eda.py`, `hemidirection.py`, `style.py`.
- All fitting is NON-LINEAR regression via lmfit, reporting parameter confidence intervals, R^2, reduced chi-squared, RMSE and AIC.
- Every function that produces a reportable number writes it toward `data/processed/`, never to a figure caption directly.

## What must never go here

- Linearised isotherm or kinetic transforms as the production fitting route. Linearisation distorts the error structure (Tran et al. 2017); it appears ONLY in the appendix comparison.
- Hard-coded numbers of any kind.
