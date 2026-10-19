# Simulations

Monte Carlo model of XEN, DBXen and the Granary, plus the HALF-LIGHT season simulator. See [docs/model/simulations.md](../docs/model/simulations.md) for the results and their limits.

## Requirements

Python 3 with numpy and matplotlib:

```bash
pip install numpy matplotlib
```

## Files

| File | What it does |
| --- | --- |
| `hyperstructure_sim.py` | The model: `simulate()`, `draw_priors()`, `deflation_day()` |
| `run_scenarios.py` | Main scenarios and the overview chart (`sim_overview.png`) |
| `sensitivity.py` | Which inputs drive the results |
| `final_checks.py` | Release horizon and diversion vs new-demand checks |
| `release_rule.py` | Release rule comparisons |
| `game_scoring.py` | Tribe scoring checks (plain sum vs quadratic, concentration) |
| `*.json` | Saved results of the runs above |
| `game/half-light-simulator.html` | Season simulator: open in a browser, play as one tribe against AI tribes |

## Change the assumptions

Every market input is a guessed range in `draw_priors()` in `hyperstructure_sim.py`. Replace them with on-chain measurements or your own ranges, rerun, and post what you find with the **Simulation result** issue template.
