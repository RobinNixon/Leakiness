# Negative Results: Failed Capacity Metrics

This document records metrics that were investigated as potential second-axis (capacity) predictors but failed to reliably separate life-like-prone from resistant substrates. These negative results are valuable for understanding what does NOT work and why.

## 1. Motif Density (Phase 11-12)

### Initial Promise

Motif density—the frequency of recurring spacetime patterns—initially achieved perfect separation (AUC = 1.0) between prone and resistant substrates.

**Counter-intuitive finding**: Prone substrates had LOWER motif density than resistant substrates. This inverted the intuition that "prone rules have gliders/patterns."

### The Problem: Parameter Sensitivity

When we varied measurement parameters, the metric failed catastrophically:

| Window Size | AUC | Direction |
|-------------|-----|-----------|
| 3×5 | 0.007 | INVERTED |
| 3×10 | 0.891 | Correct |
| 3×20 | 1.000 | Correct |
| 5×10 | 1.000 | Correct |

**The direction INVERTS with window size!**

At small windows (3×5):
- Additive rules (90, 150) have HIGH motif density (period-2 patterns fit in small windows)
- Prone substrates have LOW density

At larger windows (3×20):
- Additive rules have NEAR-ZERO density (no patterns persist that long)
- Prone substrates have MODERATE density (gliders create recurring motifs)

### Time Horizon Degradation

| Time Horizon | AUC | Issue |
|--------------|-----|-------|
| T=100 | 0.999 | Works |
| T=200 | 0.963 | Works |
| T=500 | 0.778 | Degraded |

At T=500, Rule 30 density rises to match prone substrates, causing overlap.

### Conclusion

**Motif density is NOT a robust metric.** The AUC = 1.0 was an artifact of specific parameter choices (3×10 window, T=300). No single threshold achieves >90% accuracy across all conditions.

**Why it fails**: Recurring motifs measure periodicity, not capacity for life-like structure. Additive rules have many short-period motifs; complex rules have few but meaningful ones.

---

## 2. Cell-Level Mutual Information (Phase 13)

### Hypothesis

Prone substrates should show intermediate-term memory (slow I(δ) decay), while resistant substrates either lose information fast (chaotic) or preserve only trivial short-period information (additive).

### The Problem: All Curves Are Flat

| Substrate | I(1) | I(8) | I(64) | Prone |
|-----------|------|------|-------|-------|
| Rule 110 | 0.016 | 0.016 | 0.016 | YES |
| Rule 54 | 0.014 | 0.015 | 0.016 | YES |
| 2D CA | 0.012 | 0.015 | 0.011 | YES |
| Rule 30 | 0.013 | 0.015 | 0.012 | NO |
| Rule 90 | 0.015 | 0.015 | 0.015 | NO |
| Rule 150 | 0.015 | 0.015 | 0.016 | NO |

**All substrates show MI ~ 0.012-0.016 regardless of lag or classification.**

### Capacity Score Comparison

| Score Type | AUC | Issue |
|------------|-----|-------|
| Area under I(δ) | 0.667 | Near random |
| Half-life | 1.000* | Degenerate |
| Bandpass | 0.667 | Near random |

*Half-life = 64 for ALL substrates (degenerate—no decay detected).

### Why It Fails

1. **Cell-level MI doesn't capture pattern structure**: Gliders involve coordinated multi-cell patterns; individual cell correlations look similar across rules.

2. **Subsampling destroys spatial information**: Random 50-cell subsample loses pattern structure.

3. **Noise floor dominates**: Binary cells have limited entropy; signal-to-noise is poor at these lags.

### Conclusion

**Cell-level mutual information does NOT separate prone from resistant substrates.** The measurement captures noise-floor correlations, not the pattern-level structure that distinguishes glider-supporting rules.

---

## 3. Roughness Metric (Phase 2)

### Initial Finding

Roughness correlated POSITIVELY (r = +0.27) with life-like %, opposite to expectation.

### Root Causes

1. **Dimensional bias**: Cosine similarity on 3200 dimensions (Semantic Vectors) is insensitive to local perturbations.

2. **Non-comparable perturbation sizes**: Binary 1D perturbs 1% of state; 2D perturbs 0.25%.

### Conclusion

**Roughness was dropped from the model.** It's a measurement artifact, not a real signal.

---

## What These Failures Teach Us

1. **Parameter sensitivity is fatal**: Metrics that invert direction with parameter changes are unusable.

2. **Cell-level ≠ pattern-level**: Single-cell statistics miss coordinated multi-cell phenomena.

3. **Intuition can mislead**: "More patterns = more life-like" was wrong; structure matters more than frequency.

4. **Simplicity wins**: Compression is parameter-free and captures exactly what we need—algorithmic complexity at the pattern level.

---

## Recommendations for Future Work

If investigating alternative capacity metrics:

1. **Test across window sizes**: Any metric must be robust to 2× changes in measurement parameters.

2. **Check for direction stability**: If the metric inverts, it's measuring an artifact.

3. **Use pattern-aware methods**: Block entropy, transfer entropy, or other methods that capture spatial structure.

4. **Prefer scale-invariant metrics**: Compression has no tunable parameters beyond compressor choice.
