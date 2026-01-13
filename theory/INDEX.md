# Theory Files Index

This folder contains the theoretical foundations for the Substrate Leakiness framework.

## Core Theory

The two-axis framework predicts life-like behavior from substrate properties:

### Axis 1: Leakiness
How readily perturbations escape and amplify.

| Metric | Description | Weight |
|--------|-------------|--------|
| Lyapunov Growth | Perturbation amplification over time | 33% |
| Escape Dimensions | Independent directions perturbations travel | 29% |
| Branching Factor | Cells affected per perturbation step | 28% |
| State Channels | Extra states for perturbation hiding | 10% |

**Predictive Formula:**
```
Leakiness = 0.33·L + 0.29·E + 0.28·B + 0.10·C
```

### Axis 2: Capacity
Whether the substrate has sufficient structural complexity.

**Threshold:** Compression < 1.1 bits/cell → PRONE; ≥ 1.1 → RESISTANT

## Key Results

1. **Leakiness predicts life-like %** with R² = 0.96 and perfect rank correlation
2. **Stickiness operates as temporal filter** with acceptance ratio ~1/d
3. **Two-point calibration** predicts optimal depth with r = 0.996
4. **Compression separates** prone from resistant with AUC = 0.944

## The Complete Protocol

```
1. Measure activity and compression (pre-screening)
2. If PRONE: perform two-point Lyapunov calibration
3. Apply predicted confirmation depth d*
4. Life-like behavior emerges
```

## Files

See `data/PROGRESS.md` for complete research log and `data/RESULTS_SUMMARY.md` for findings overview.
