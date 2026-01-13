# Leakiness as a Predictor of Life-Like Behavior

## Summary

**Leakiness** - the ease with which perturbations escape, dissipate, or amplify - predicts life-like percentage across substrates with R² = 0.96.

Substrates that "hold" perturbations (tight vessels) become life-like easily. Substrates that "leak" perturbations (loose vessels) resist life-like behavior.

---

## Leakiness Metrics

Four metrics capture three dimensions of perturbation dynamics:

| Dimension | Metric | What it measures |
|-----------|--------|------------------|
| **Temporal** | Lyapunov Growth | Perturbation amplification over time |
| **Spatial** | Escape Dimensions | Independent directions perturbations can travel |
| **Combinatorial** | Branching Factor | Cells affected by single perturbation per step |
| **Capacity** | State Channels | Extra states where perturbations can hide |

---

## Results

### Metrics Table

| Substrate | Lyapunov | Escape | Branching | Channels | Life-Like % |
|-----------|----------|--------|-----------|----------|-------------|
| Discretized Vector Fields | **-0.109** | 2.0 | 1.30 | 0.30 | 100.0% |
| Binary 1D ECA | 0.177 | 2.0 | 1.73 | 0.00 | 83.7% |
| Semantic Vectors | 0.078 | 10.0 | 1.00 | 0.50 | 39.0% |
| Ternary CA | 0.152 | 2.0 | 2.64 | 1.00 | 36.7% |
| 2D Binary CA | 0.359 | 8.0 | 3.31 | 0.00 | 17.5% |

### Metric Correlations with Life-Like %

| Metric | Correlation | Weight in Model |
|--------|-------------|-----------------|
| Lyapunov Growth (Temporal) | r = -0.75 | 33% |
| Escape Dimensions (Spatial) | r = -0.66 | 29% |
| Branching Factor (Combinatorial) | r = -0.63 | 28% |
| State Channels (Capacity) | r = -0.23 | 10% |

All correlations are **negative** (inverse): higher leakiness = lower life-like %.

### Aggregate Leakiness

| Substrate | Leakiness Score | Life-Like % |
|-----------|-----------------|-------------|
| Discretized Vector Fields | 0.07 | 100.0% |
| Binary 1D ECA | 0.29 | 83.7% |
| Semantic Vectors | 0.47 | 39.0% |
| Ternary CA | 0.48 | 36.7% |
| 2D Binary CA | 0.82 | 17.5% |

**Rank correlation: rho = -1.0 (perfect)**

---

## Predictive Model

### Sigmoid Phase Transition

```
Life-Like % = 115 / (1 + exp(6.5 * (L - 0.39)))
```

- **R² = 0.96** (explains 96% of variance)
- **Phase transition at L = 0.39**: substrates below this threshold can become highly life-like; substrates above it are constrained

### Model Weights

```
Leakiness = 0.33*Lyapunov_n + 0.29*Escape_n + 0.28*Branching_n + 0.10*Channels_n
```

Where `_n` denotes min-max normalization.

---

## Key Findings

### 1. Lyapunov Growth Dominates

The temporal dimension (perturbation growth over time) is the strongest predictor. Critically, **Discretized Vector Fields has negative Lyapunov growth** (-0.109), meaning perturbations actively contract rather than expand. This makes it an "active suppressor" of perturbations, explaining its 100% life-like rate.

### 2. Spatial and Combinatorial Dimensions Add Information

- **Escape Dimensions**: 2D CA (8 directions) and Semantic Vectors (10 effective dimensions) leak perturbations in more directions than 1D systems (2 directions)
- **Branching Factor**: 2D CA spreads perturbations to 3.3 cells per step vs 1.3 for Vector Fields

### 3. Phase Transition Structure

The sigmoid relationship indicates a threshold effect: below L ~ 0.4, substrates readily become life-like; above it, life-like behavior becomes increasingly difficult to achieve.

---

## Interpretation

Leakiness captures how well a substrate acts as a "vessel" for perturbations:

```
TIGHT VESSELS                      LOOSE VESSELS
(low leakiness)                    (high leakiness)
      |                                  |
      v                                  v
 Vector Fields                      2D Binary CA
 L = 0.07                           L = 0.82
      |                                  |
      v                                  v
 Perturbations                      Perturbations
 CONTRACT                           EXPAND rapidly
      |                                  |
      v                                  v
 100% life-like                     17.5% life-like
```

The three primary metrics capture complementary aspects:
- **Temporal**: Does a perturbation grow or shrink over time?
- **Spatial**: How many escape routes exist?
- **Combinatorial**: How many cells are immediately affected?

Together, these determine whether a substrate can "hold" the coherent patterns necessary for life-like behavior.

---

## Conclusion

Leakiness explains substrate variation in life-like behavior. The aggregate leakiness score achieves perfect rank correlation (rho = -1.0) with life-like percentage, and the sigmoid model captures 96% of the variance.

The central insight: **a substrate's intrinsic tendency to amplify or suppress perturbations over time (Lyapunov) is the primary determinant of how easily it can be made life-like**, with spatial escape routes and combinatorial branching as secondary factors.
