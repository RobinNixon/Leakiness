# Substrate Leakiness Predicts Life-Like Behavior

A framework for predicting and engineering self-maintaining behavior in discrete dynamical systems.

## Key Findings

1. **Leakiness** (Lyapunov + escape dimensions + branching) predicts life-like percentage with R² = 0.96
2. **Stickiness** works via temporal filtering, not spatial selectivity
3. **Two-point calibration** predicts optimal confirmation depth from just 2 measurements (r = 0.996)
4. **Compression ratio** separates life-like-prone from resistant substrates (AUC = 0.944)

## The Two-Axis Framework

| Axis | Metric | What It Predicts |
|------|--------|------------------|
| Leakiness | Lyapunov + Escape + Branching | HOW MUCH stickiness is needed (d*) |
| Capacity | Compression (bits/cell) | WHETHER stickiness will work |

## The Complete Protocol

```
┌─────────────────────────────────────┐
│     Substrate at d=1                │
└─────────────────┬───────────────────┘
                  │
                  ▼
        ┌─────────────────┐
        │ Activity > 1%   │
        │ OR Lyapunov > 0?│
        └────────┬────────┘
                 │
         NO ◄────┴────► YES
          │              │
          ▼              ▼
    ┌──────────┐   ┌─────────────────┐
    │ RESISTANT│   │ Compression     │
    │  (dead)  │   │ < 1.1 bits/cell?│
    └──────────┘   └────────┬────────┘
                            │
                    NO ◄────┴────► YES
                     │              │
                     ▼              ▼
               ┌──────────┐   ┌──────────┐
               │ RESISTANT│   │  PRONE   │
               │ (chaotic)│   │(proceed) │
               └──────────┘   └────┬─────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ Two-point calibration:   │
                    │ 1. Measure L₀ at d=1     │
                    │ 2. Measure L₄ at d=4     │
                    │ 3. γ = log ratio / log 4 │
                    │ 4. d* = (L₀/L_crit)^(1/γ)│
                    └──────────────────────────┘
```

## Quick Start

```python
from protocol_implementation import predict_lifelike

# For any ECA rule
result = predict_lifelike(rule=110)
print(f"Classification: {result['classification']}")
print(f"Optimal depth: {result['d_star']}")
print(f"Expected life-like: {result['expected_lifelike']}")
```

## Repository Structure

```
Leakiness/
├── paper/
│   ├── substrate_leakiness.tex     # Full paper (LaTeX) with figures
│   ├── substrate_leakiness.md      # Full paper (Markdown)
│   ├── references.bib              # Bibliography
│   └── figures/
│       ├── fig1_leakiness_vs_lifelike.png
│       ├── fig2_temporal_filter_signature.png
│       ├── fig3_depth_prediction.png
│       ├── fig4_two_axis_framework.png
│       ├── fig5_generalization_validation.png
│       ├── fig6_validation_pooled.png
│       └── FIGURE_CAPTIONS.md
├── code/
│   └── protocol_implementation.py  # Reference implementation
├── data/
│   ├── substrate_metrics.csv       # All 50 rules with metrics
│   ├── depth_sweep_results.csv     # Calibration data
│   ├── validation_results.csv      # Validation results
│   ├── PROGRESS.md                 # Research progress log
│   └── RESULTS_SUMMARY.md          # Key findings summary
├── theory/
│   └── INDEX.md                    # Theory overview
├── supplementary/
│   ├── methods_detail.md           # Extended methodology
│   ├── all_rules_table.md          # Complete 50-rule results
│   └── negative_results.md         # Failed metrics documentation
├── discussion/
│   ├── INDEX.md                    # Discussion index
│   ├── IMPLICATIONS.md             # Implications
│   └── FUTURE_WORK.md              # Open problems
├── LICENSE
├── README.md                       # This file
└── substrate_leakiness.pdf         # PDF of the paper
```

## Key Equations

### Weighted Leakiness
```
Leakiness = 0.33·L + 0.29·E + 0.28·B + 0.10·C
```
Where: L = Lyapunov, E = Escape dimensions, B = Branching, C = Channels

### Sigmoid Prediction
```
Life-Like % = 115 / (1 + exp(6.5·(L - 0.39)))
```
Achieves R² = 0.956

### Power-Law Decay
```
L(d) = L_min + (L₀ - L_min)·d^(-γ)
```

### Optimal Depth Control Law
```
d* = ((L₀ - L_min) / (L_crit - L_min))^(1/γ)
```
With L_min ≈ -0.05, L_crit ≈ 0.05

### Two-Point Gamma Estimation
```
γ = log((L₀ + 0.05) / (L₄ + 0.05)) / log(4)
```
Correlation with full fit: r = 0.996

## Results Summary

### Original 6 Substrates

| Substrate | Leakiness | Life-Like % | Compression | Classification |
|-----------|-----------|-------------|-------------|----------------|
| Vector Field | 0.22 | 100.0% | 0.45 | Prone |
| Rule 110 | 0.35 | 83.7% | 0.95 | Prone |
| Semantic | 0.42 | 39.0% | 0.82 | Prone |
| Ternary | 0.53 | 36.7% | 0.91 | Prone |
| 2D CA | 0.64 | 17.5% | 0.51 | Prone |

### Expanded Validation (50 Rules)

| Metric | Value |
|--------|-------|
| Accuracy | 86.7% |
| AUC (active rules) | 0.944 |
| False Positive Rate | 16.7% |
| False Negative Rate | 0.0% |

## Citation

```bibtex
@article{nixon2026leakiness,
  title={Substrate Leakiness Predicts Life-Like Behavior: A Two-Axis Framework
         for Engineering Self-Maintenance in Discrete Dynamical Systems},
  author={Nixon, Robin},
  year={2026},
  note={Preprint}
}
```

## Related Work

- Wolfram, S. (2002). A New Kind of Science
- Langton, C. G. (1990). Computation at the edge of chaos
- Cook, M. (2004). Universality in elementary cellular automata

## License

MIT License

## Acknowledgments

This research was conducted with assistance from Claude (Anthropic), which contributed to experimental design, code implementation, and analysis. All conclusions and interpretations are the author's own.
