# Leakiness Investigation Progress Log

## Project: Measuring Leakiness as a Predictor of Life-Like Behavior

**Core Hypothesis**: Life-like % is inversely related to substrate leakiness. Substrates that "hold" perturbations (tight vessels) become life-like easily; substrates that "leak" perturbations (loose vessels) resist life-like behavior.

---

## Session 1: Initial Analysis and Roughness Investigation

### Phase 1: Initial Leakiness Framework
**Status**: Complete

Developed measurement framework with 5 candidate metrics as projections of latent "leakiness":

1. **Perturbation Branching Factor** - cells affected by single flip after one step
2. **Lyapunov-like Growth Rate** - perturbation amplification over N steps
3. **Escape Dimensions** - independent directions perturbations can travel
4. **State Leakage Channels** - extra states where perturbations can hide
5. **Geometric Roughness** - inverse of dynamics smoothness

**Initial Results (5 metrics)**:

| Substrate | Branch | Lyapunov | Escape | Channels | Roughness | Life-Like % |
|-----------|--------|----------|--------|----------|-----------|-------------|
| Discretized VF | 1.30 | -0.109 | 2.0 | 0.30 | 0.014 | 100.0% |
| Binary 1D ECA | 1.72 | 0.149 | 2.0 | 0.00 | 0.017 | 83.7% |
| Semantic Vectors | 1.00 | 0.061 | 10.0 | 0.50 | 0.001 | 39.0% |
| Ternary CA | 2.64 | 0.216 | 2.0 | 1.00 | 0.025 | 36.7% |
| 2D Binary CA | 3.45 | 0.321 | 8.0 | 0.00 | 0.008 | 17.5% |

**Key Finding**: Weighted leakiness achieved perfect rank correlation (rho = -1.0) with life-like %.

---

### Phase 2: Roughness Anomaly Investigation
**Status**: Complete

**Problem Identified**: Roughness correlated POSITIVELY (r = +0.27) with life-like %, opposite to expectation.

**Investigation Conducted**:
- Documented original methodology
- Analyzed cross-substrate measurement consistency
- Tested alternative hypotheses (U-shaped, interactions, outliers)
- Designed and computed improved roughness metrics

**Root Causes Identified**:

1. **Dimensional bias in similarity metric**
   - Cosine similarity on 3200 dimensions (Semantic Vectors) insensitive to local perturbations
   - Artificially reports "smooth" for high-dimensional substrates

2. **Non-comparable perturbation sizes**
   - Binary 1D ECA: 1.0% of state perturbed
   - 2D Binary CA: 0.25% of state perturbed
   - Semantic Vectors: ~0.1% effective change

**Falsification Evidence**: Smoothest (Semantic: 0.001) and second-smoothest (2D CA: 0.008) substrates at opposite extremes of life-like % (39% vs 17.5%).

**Decision**: Drop roughness from the model - measurement artifact, not real signal.

---

### Phase 3: Revised 4-Metric Model
**Status**: Complete

Removed roughness, retaining 4 metrics capturing 3 dimensions of perturbation dynamics:

| Dimension | Metric | Correlation with Life-Like % |
|-----------|--------|------------------------------|
| Temporal | Lyapunov Growth | r = -0.75 |
| Spatial | Escape Dimensions | r = -0.66 |
| Combinatorial | Branching Factor | r = -0.63 |
| Capacity | State Channels | r = -0.23 |

**Improved Results**:

| Metric | v1 (5 metrics) | v2 (4 metrics) |
|--------|---------------|----------------|
| Pearson (simple) | r = -0.856 | **r = -0.992** |
| Spearman | rho = -1.000 | rho = -1.000 |
| Best R² | 0.903 | **0.956** |

**Predictive Formula** (Sigmoid, R² = 0.956):
```
Life-Like % = 115 / (1 + exp(6.5 * (L - 0.39)))
```

**Model Weights**:
- Lyapunov Growth: 33%
- Escape Dimensions: 29%
- Branching Factor: 28%
- State Channels: 10%

---

### Phase 4: Why Vector Fields Has Negative Lyapunov
**Status**: Complete

**Question**: Why does Discretized Vector Fields achieve negative Lyapunov (-0.109)?

**Answer**: Alignment/consensus dynamics are fundamentally **contractive**.

```python
# Vector Field update rule
votes = count_directions(left, center, right)
if center has max votes:
    stay
else:
    move one step toward most popular direction
```

**Mechanism**: Perturbations get "voted out" by neighbors - the outlier direction is pulled back toward local consensus.

**Physical Analogy**:
| System | Lyapunov | Behavior |
|--------|----------|----------|
| Vector Field alignment | Negative | Like viscous damping |
| Heat diffusion | Negative | Temperature gradients decay |
| Game of Life | Positive | Small changes cascade |

**Key Insight**: Vector Fields don't just avoid amplifying perturbations - they actively **suppress** them. The substrate is already "trying" to reach coherence.

---

### Phase 5: Can Other Substrates Be Made Contractive?
**Status**: Complete

**Question**: Can positive-Lyapunov substrates be modified to achieve negative Lyapunov?

**Modifications Tested**:
1. Majority voting
2. Damped updates (probabilistic state retention)
3. Diffusive coupling (continuous internal state)
4. Hybrid blending (ECA + Majority)
5. Local averaging with threshold

**Results**:

| Modification | Binary 1D | Binary 2D | Achieves Contraction? |
|--------------|-----------|-----------|----------------------|
| Baseline | +0.19 | +0.29 | No |
| Majority Voting | **-0.22** | **-0.24** | **Yes** |
| Damping (0.9) | +0.34 | +0.49 | No |
| Local Averaging | — | **-0.40** | **Yes** |

**Critical Finding - The Contraction-Activity Tradeoff**:

```
Pure ECA (Lyap=+0.19):      Activity = 42%
Pure Majority (Lyap=-0.25): Activity = 1%
```

**Tight vessels are boring.** Contraction kills computational richness.

**Key Answers**:
- Binary substrates CAN achieve negative Lyapunov (with majority dynamics)
- There IS a continuum from positive to negative (via hybrid blending)
- Contraction does NOT preserve computational richness
- Rule structure (information propagation vs consensus) determines Lyapunov sign

---

### Phase 6: Selective Damping Hypothesis
**Status**: Complete

**Hypothesis**: Stickiness achieves contraction selectively - suppressing perturbations at boundaries while preserving dynamics in bulk regions.

**Four Experiments Conducted**:

**A. Spatial Selectivity Map**
- Measured boundary vs bulk suppression rates
- Result: Sticky ECA shows NO spatial selectivity (0.0x ratio)
- Majority blend also non-selective

**B. Activity-Matched Comparison**

| System | Lyapunov | Activity |
|--------|----------|----------|
| Standard ECA | +0.19 | 42.5% |
| Sticky ECA (d=2) | +0.12 | **20.4%** |
| Majority Blend (99%) | +0.17 | 1.0% |

**Sticky preserves 20x more activity than majority at similar Lyapunov.**

**C. Local Lyapunov Decomposition**
- Measured local Lyapunov at boundaries vs bulk
- No clear spatial differential for sticky ECA
- Majority blend shows uniform contraction

**D. Model Generalization**
- Tested hybrid substrates against sigmoid model
- Mixed results (proxy metric, not full classification)

**Hypothesis Verdict**: 1/3 criteria confirmed. Spatial selectivity NOT supported.

**Revised Understanding**:

Stickiness is **TEMPORAL filtering**, not **SPATIAL filtering**.

```
Majority Voting:              Stickiness:
  "What do neighbors say?"      "Does rule want change?"
  -> Immediate consensus        -> Increment counter if yes
  -> Kills ALL dynamics         -> Change only if confirmed N times
                                -> Preserves transient dynamics
```

**Revised Mechanistic Bridge**:
```
Stickiness
    -> Temporal inertia (confirmation depth)
    -> Filters noise, preserves signal
    -> Allows transient pattern formation
    -> Suppresses only sustained divergence
    -> Tight vessel WITH activity
    -> Life-like behavior
```

**Design Principle**: To tighten a leaky vessel without killing dynamics, add **temporal confirmation** rather than **spatial consensus**.

---

### Phase 7: Temporal Filter Characterization
**Status**: Complete

**Hypothesis**: Stickiness acts as a temporal low-pass filter - it blocks short-lived update pressures while allowing sustained pressures through. Confirmation depth is the cutoff frequency.

**Experiment**: Confirmation depth sweep (d = 1, 2, 3, 4, 6, 8, 12)

**Key Results**:

| Depth | Lyapunov | Activity | Attempt Rate | Acceptance Ratio |
|-------|----------|----------|--------------|------------------|
| 1 | 0.111 | 42.4% | 42.4% | 100.0% |
| 2 | 0.112 | 21.0% | 42.1% | 50.0% |
| 3 | 0.069 | 13.9% | 41.7% | 33.4% |
| 4 | 0.080 | 10.4% | 41.5% | 25.0% |
| 6 | 0.059 | 7.0% | 41.5% | 16.8% |
| 8 | 0.034 | 5.2% | 41.3% | 12.6% |
| 12 | 0.035 | 3.5% | 41.3% | 8.4% |

**Critical Finding - The Temporal Filter Signature**:

1. **Attempt rate stays constant (~42%)** - the rule still "wants" to change cells at the same rate regardless of depth
2. **Acceptance ratio drops as 1/d** - acceptance ≈ 100%/d (perfect filter behavior)
3. **Lyapunov decreases** from +0.11 to +0.03 (69% reduction)
4. **Activity decreases** from 42% to 3.5% (92% reduction)

**Acceptance Curve Threshold Behavior**:
- P(execute | run_length = k) shows sharp threshold at k = d
- Short-lived pressures (k < d) are completely blocked
- Sustained pressures (k >= d) get through

**Prediction Confirmation** (2/2 criteria met):
- [CONFIRMED] Attempt rate stable while acceptance ratio drops
- [CONFIRMED] Can reduce Lyapunov while retaining some activity

**Interpretation**:

Stickiness is a **temporal low-pass filter**:
```
              Frequency Domain

High freq     ████████░░░░░░░░    Blocked (transient noise)
(short runs)

Low freq      ░░░░░░░░████████    Passed (sustained signal)
(long runs)

              ←── d sets cutoff ──→
```

**Quantitative Policy Dial**:
```
depth → filter cutoff → effective leakiness → life-like prevalence
```

This transforms stickiness from a phenomenological observation into a tunable parameter with predictable effects.

---

### Phase 8: Optimal Depth Prediction from Baseline Lyapunov
**Status**: Complete

**Goal**: Turn stickiness from a discovered mechanism into a predictive control law: given a substrate's baseline Lyapunov, predict the minimum confirmation depth required to enter the life-like regime.

**Experimental Design**:
- 6 substrates with varying baseline Lyapunov: Rule 110, 30, 90, 54, 150 (1D ECAs), 2D CA (Game of Life)
- Sparse depth sweeps: d = 1, 2, 4, 8, 12
- Power-law model: L(d) = L_min + (L_0 - L_min) * d^(-gamma)
- Prediction formula: d* = ((L_0 - L_min) / (L_crit - L_min))^(1/gamma)

**Key Results**:

| Substrate | L_0 | L_min | gamma | R^2 |
|-----------|-----|-------|-------|-----|
| Rule 110 (complex) | +0.138 | +0.004 | 0.56 | 0.962 |
| Rule 30 (chaotic) | +0.155 | -0.061 | 0.32 | 0.982 |
| Rule 90 (fractal) | +0.185 | -0.112 | 0.27 | 0.987 |
| Rule 54 (complex) | +0.081 | -0.090 | 0.10 | 0.568 |
| Rule 150 (additive) | +0.203 | -0.023 | 0.37 | 0.985 |
| 2D CA (GoL) | +0.178 | -0.015 | 5.00 | 0.919 |

**Prediction Accuracy**:

| Substrate | d_pred | d_obs | Error |
|-----------|--------|-------|-------|
| Rule 110 | 6.8 | 8 | 1.2 |
| Rule 30 | 7.8 | 8 | 0.2 |
| Rule 90 | 9.3 | 8 | 1.3 |
| Rule 54 | 7.3 | 4 | 3.3 |
| 2D CA | 1.2 | 2 | 0.8 |

Mean absolute error: 1.35 depth units

**Critical Finding - Gamma Is NOT Universal**:

Gamma coefficient of variation = 1.58, indicating significant substrate-dependent variation.

This means:
1. The power-law decay model fits individual substrates well (R^2 > 0.96 for most)
2. BUT gamma varies substantially between substrates (0.1 to 5.0)
3. A universal control law requires substrate-specific gamma calibration
4. Alternatively, a two-measurement protocol: measure at d=1 and d=4 to estimate gamma

**Anomalous Substrates**:
- **Rule 54**: Poor fit (R^2 = 0.57) - Lyapunov drops then rises slightly, non-monotonic
- **2D CA**: Very high gamma (5.0) - extremely rapid decay, possibly due to different dynamics (extinction vs pattern propagation)

**Control Law** (with substrate-specific parameters):
```
d* = ((L_0 - L_min) / (L_crit - L_min))^(1/gamma)

Where:
  L_crit = 0.05   (life-like threshold)
  L_min  ~ -0.05  (asymptotic minimum, substrate-dependent)
  gamma  ~ 0.3-0.6 for 1D ECAs (substrate-dependent)
```

**Simplified Rule of Thumb** (for typical 1D ECAs):
```
d* ~ 10-30 * L_0  (linear approximation)
```

**Success Criteria Evaluation**:
- [CONFIRMED] Optimal depth scales predictably with baseline Lyapunov (mean error 1.35)
- [PARTIAL] Gamma shows variation (CV = 1.58) - not a universal constant

---

### Phase 9: Predict Gamma from Baseline Substrate Properties
**Status**: Complete

**Goal**: Determine whether gamma (filter efficiency) can be inferred from baseline substrate measurements without fitting the full depth curve.

**Hypothesis**: Gamma encodes how efficiently temporal filtering suppresses divergence. Primary candidate: Escape dimensions (spatial degrees of freedom).

**Experimental Design**:
- Two-point gamma estimation: gamma_est = log((L0 - L_min) / (L4 - L_min)) / log(4)
- Correlation analysis: Each baseline metric vs gamma
- Regression models: Single and multiple predictors

**Key Results**:

**Two-Point Estimation** (comparing gamma_est from d=1,4 vs gamma_fitted from full sweep):

| Substrate | L(d=1) | L(d=4) | gamma_est | gamma_fit | Match |
|-----------|--------|--------|-----------|-----------|-------|
| Rule 110 | +0.110 | +0.069 | 0.243 | 0.260 | OK |
| Rule 30 | +0.129 | +0.075 | 0.239 | 0.234 | OK |
| Rule 90 | +0.069 | +0.069 | 0.010 | 0.010 | OK |
| Rule 54 | +0.093 | +0.075 | 0.022 | 0.035 | OK |
| Rule 150 | +0.110 | +0.110 | 0.010 | 0.027 | OK |
| 2D CA | +0.191 | +0.152 | 0.041 | 0.063 | OK |

**Two-point vs Full-fit correlation: r = 0.996** - Excellent agreement!

**Correlation Analysis** (Baseline Metrics vs Gamma):

| Predictor | r | R^2 | p-value | Interpretation |
|-----------|---|-----|---------|----------------|
| L0 | +0.19 | 0.04 | 0.71 | Not significant |
| Branching | -0.41 | 0.17 | 0.42 | Not significant |
| Escape | -0.18 | 0.03 | 0.73 | Not significant |
| Activity | -0.12 | 0.02 | 0.82 | Not significant |

**Critical Finding - Escape Hypothesis NOT Supported**:
- Escape dimensions do not predict gamma (R^2 = 0.033, p = 0.73)
- No single baseline metric explains gamma (all R^2 < 0.2)
- Multiple regression (L0 + Escape) achieves R^2 = 0.49, still insufficient

**But Two-Point Estimation Works Perfectly**:
- Correlation between two-point and full-fit: r = 0.996
- Mean absolute error: 0.012
- Only TWO measurements (d=1, d=4) needed to calibrate gamma

**Success Criteria Evaluation**:
- [FAILED] Single predictor R^2 > 0.7 (best: Branching at R^2 = 0.17)
- [CONFIRMED] Two-point estimation matches full fit (r = 0.996)
- [NOT TESTED] Held-out validation (insufficient variation in substrate types)

**Final Verdict: (B) TWO-STEP PROTOCOL**

Gamma cannot be predicted from baseline substrate properties alone, but can be accurately estimated from just two Lyapunov measurements at d=1 and d=4.

The complete predictive protocol is:
```
1. Measure baseline Lyapunov L0 (at d=1)
2. Measure Lyapunov at d=4 (L4)
3. Estimate gamma: gamma = log((L0 - L_min) / (L4 - L_min)) / log(4)
4. Predict optimal depth: d* = ((L0 - L_min) / (L_crit - L_min))^(1/gamma)
```

This is a "minimal calibration" result - gamma is an irreducible substrate property, but only 2 measurements are needed to characterize it.

---

### Phase 10: End-to-End Validation of the Two-Point Protocol
**Status**: Complete

**Goal**: Demonstrate that the two-point calibrated control law predicts the depth at which life-like behavior emerges.

**Protocol**:
1. Two-point calibration: Measure L0, L4, estimate gamma, predict d*
2. Validation sweep: depths around d* (+/-2)
3. Measure life-like %, activity, Lyapunov at each depth

**Calibration Results**:

| Substrate | L0 | L4 | gamma | d* |
|-----------|-----|-----|-------|-----|
| Rule 110 | +0.113 | +0.069 | 0.23 | 8.4 |
| Rule 30 | +0.129 | +0.074 | 0.26 | 9.0 |
| Rule 90 | +0.069 | +0.069 | 0.30 | 1.8 |
| Rule 150 | +0.110 | +0.110 | 0.30 | 4.8 |
| 2D CA | +0.178 | +0.137 | 0.14 | 20.0 |
| Rule 54 | +0.110 | +0.070 | 0.21 | 9.4 |

**Validation Results**:

| Substrate | Predicted d* | Observed Onset | Error | Status |
|-----------|-------------|----------------|-------|--------|
| Rule 110 | 8.4 | 6 | 2.4 | CLOSE |
| Rule 30 | 9.0 | 11 | 2.0 | OK |
| Rule 90 | 1.8 | 4 | 2.2 | CLOSE |
| Rule 150 | 4.8 | 7 | 2.2 | CLOSE |
| 2D CA | 20.0 | 18 | 2.0 | OK |
| Rule 54 | 9.4 | 7 | 2.4 | CLOSE |

**Statistics**:
- Mean Absolute Error: 2.20
- Within +/-2: 2/6 (33%)
- Within +/-3: 6/6 (100%)
- Life-like saturates at/before d*: 6/6
- Activity continues falling past d*: 4/6

**Key Finding - Substrates Split Into Two Groups**:

1. **Life-like prone** (Rule 110, Rule 54, 2D CA): Already at 100% life-like well before predicted d*
2. **Life-like resistant** (Rule 30, Rule 90, Rule 150): Never exceed ~20% life-like at any depth

This reveals that **life-like potential is substrate-intrinsic**:
- Some substrates WILL become life-like with sufficient depth
- Some substrates NEVER become life-like regardless of depth
- The control law predicts where Lyapunov crosses threshold, not onset

**Saturation Behavior Confirmed**:
- Life-like % saturates at or before d* for all substrates
- Activity continues falling past d* (diminishing returns)
- Beyond d*, you pay activity cost without life-like gain

**Success Criteria Evaluation**:
- [PARTIAL] Life-like onset within +/-2 for 2/6 substrates
- [CONFIRMED] All substrates within +/-3
- [CONFIRMED] Saturation pattern: Life-like saturates while activity falls
- [PARTIAL] Moderate clustering around identity (MAE = 2.20)

**Revised Understanding**:

The control law predicts **Lyapunov threshold crossing**, which is:
- A **necessary** condition for life-like behavior (you can't be life-like with high Lyapunov)
- But NOT **sufficient** (some substrates never become life-like)

The protocol is prescriptive for **life-like-prone substrates**. For resistant substrates, additional modifications (rule structure changes) may be needed.

---

### Phase 11: Pre-Screening Metric for Prone vs Resistant Substrates
**Status**: Complete

**Goal**: Find a metric that separates prone (Rule 110, 54, 2D CA) from resistant (Rule 30, 90, 150) substrates before running full life-like classification.

**Candidate Metrics Tested**:
1. Attractor Diversity (distinct final configurations)
2. Persistent Motif Density (recurring spacetime patterns)
3. Information Storage (mutual information I(S_t; S_{t+20}))
4. Localized Object Count (discrete objects in spacetime)

**Key Results** (at d=1):

| Substrate | Prone | Attractors | Motif Density | Info (MI) | Objects |
|-----------|-------|------------|---------------|-----------|---------|
| Rule 110 | YES | 50 | 0.019 | 0.004 | 5.1 |
| Rule 54 | YES | 50 | 0.010 | 0.385 | 0.0 |
| 2D CA | YES | 50 | 0.012 | 1.706 | 10.5 |
| Rule 30 | NO | 50 | 0.051 | 0.004 | 44.3 |
| Rule 90 | NO | 50 | 0.102 | 0.006 | 24.5 |
| Rule 150 | NO | 50 | 0.102 | 0.005 | 71.3 |

**Counter-Intuitive Finding - Metrics Invert**:

| Metric | Cohen's d | AUC | Direction |
|--------|-----------|-----|-----------|
| Diversity Score | +1.95 | 1.000 | Prone > Resistant |
| Info Storage (MI) | +1.35 | 0.778 | Prone > Resistant |
| Motif Density | -4.16 | 0.000* | Prone < Resistant |
| Object Count | -2.99 | 0.000* | Prone < Resistant |

*AUC = 0.0 means perfect separation but INVERSE of expected direction

**Critical Insight - Why Metrics Invert**:

The user's intuition was that "prone rules have gliders/objects". But the measurement reveals the OPPOSITE:
- **Resistant substrates have MORE motifs and MORE "objects"** because they're chaotic/additive
- Rule 30, 90, 150 create dense activity patterns = many recurring motifs, many small objects
- **Prone substrates have FEWER but more MEANINGFUL patterns**
- Rule 110, 54, 2D CA have sparse, coherent structures (gliders) that don't register as "recurring motifs"

**The Real Separator**:

Prone substrates are characterized by:
1. **Low motif density** = Novel, non-repeating dynamics (gliders are unique, not recurring)
2. **Higher information storage** (especially 2D CA, Rule 54) = Persistent temporal correlation
3. **Lower chaotic activity** = Fewer but more coherent localized structures

Resistant substrates are characterized by:
1. **High motif density** = Repetitive, periodic patterns (additive rules repeat)
2. **Low information storage** = Chaotic forgetting
3. **High chaotic activity** = Many small, incoherent activity blobs

**Best Separator**: Diversity Score (AUC = 1.0)
- Combines attractor count with period length
- Prone substrates have longer attractor periods (richer dynamics)

**Practical Pre-Screening Rule**:
```
IF Motif Density < 0.03 THEN Prone (stickiness will work)
IF Motif Density > 0.05 THEN Resistant (stickiness won't help)
```

**Two-Axis Framework Validated**:
- **Axis 1 (Leakiness)**: Controls HOW MUCH stickiness is needed (d*)
- **Axis 2 (Capacity = inverse motif density)**: Predicts WHETHER stickiness will work

**Success Criteria**:
- [STRONG SUCCESS] Single metric achieves AUC = 1.0 (Diversity Score)
- [CONFIRMED] Clear threshold separates classes (Motif Density < 0.03)
- [CONFIRMED] Metric is not redundant with leakiness (different axis)

**NOTE**: See Phase 12 for robustness validation - motif density is NOT robust across parameter variations.

---

### Phase 12: Motif Density Robustness Validation
**Status**: Complete

**Goal**: Confirm that motif density reliably separates prone from resistant substrates across reasonable variations in measurement parameters.

**Parameter Variations Tested**:
- Initial density: p = {0.2, 0.5, 0.8}
- Window size: spatial {3, 5, 8} x temporal {5, 10, 20}
- Time horizon: T = {100, 200, 500}
- Seeds: N = 30 per condition

**Critical Finding - METRIC IS NOT ROBUST**:

| Condition | AUC | Overlap | Issue |
|-----------|-----|---------|-------|
| window=3x5 | 0.007 | 0.015 | **DIRECTION INVERTS!** |
| window=3x10 | 0.891 | 0.252 | Works (baseline) |
| window=3x20 | 1.000 | 0.000 | Works |
| window=5x10 | 1.000 | 0.000 | Works |
| T=100 | 0.999 | 0.016 | Works |
| T=200 | 0.963 | 0.100 | Works |
| T=500 | 0.778 | 0.599 | **Degraded** |

**Root Cause - Window Size Inverts Direction**:

With small temporal window (3x5):
- Rule 90, 150: HIGH motif density (0.14) - additive rules have period-2 patterns
- Prone substrates: LOW density (0.01-0.01)

With larger temporal window (3x10+):
- Rule 90, 150: NEAR-ZERO density - no patterns persist that long
- Prone substrates: MODERATE density (0.03-0.08)

**The metric's direction FLIPS based on window size!**

**Time Horizon Degradation**:

At T=500, Rule 30 density rises to match prone substrates (0.037 vs 0.031-0.045), causing overlap. Short horizons (T=100) maintain separation.

**Threshold Stability - FAILED**:

No single threshold achieves >90% accuracy across all conditions. The threshold that works for one window size fails for another because the direction inverts.

**Success Criteria**:
- [FAILED] AUC > 0.95 across all conditions (min AUC = 0.007)
- [FAILED] Threshold band achieves >95% consistently (no stable band)
- [FAILED] Distributions don't overlap (up to 60% overlap at T=500)
- [PARTIAL] Classification possible with small budget IF parameters are fixed

**Revised Conclusion**:

Motif density is **NOT** a robust pre-screening metric. The AUC = 1.0 result from Phase 11 was an artifact of specific parameter choices (3x10 window, T=300).

**What Works Instead**:
- Use **fixed window (3x20 or 5x10)** and **short horizon (T=100-200)** for reliable separation
- OR use **information storage (MI)** which showed more stable separation (AUC = 0.78 consistently)
- OR accept that prone/resistant classification may require direct life-like measurement at low depth

**Practical Recommendation**:

If using motif density for pre-screening:
1. Use window = 3x20 or 5x10 (NOT 3x5 or 3x10)
2. Use T = 100-200 steps (NOT T >= 500)
3. Threshold ~ 0.01 (prone) vs > 0.05 (resistant)

This is less robust than hoped but still usable with care.

---

### Phase 13: Information Storage as Capacity Axis
**Status**: Complete

**Goal**: Test whether mutual information I(S_t; S_{t+delta}) can serve as a robust second-axis metric to separate prone from resistant substrates.

**Hypothesis**: Prone substrates support intermediate-term memory (slow I(delta) decay), while resistant substrates either lose information fast (chaotic) or preserve only trivial short-period information (additive).

**Measurement**: For each substrate at d=1:
- Compute I(delta) for delta in {1, 2, 4, 8, 16, 32, 64}
- Test three capacity scores: Area, Half-life, Bandpass

**Results - NEGATIVE: No Separation Found**:

| Substrate | I(1) | I(8) | I(64) | Bandpass | Prone |
|-----------|------|------|-------|----------|-------|
| Rule 110 | 0.016 | 0.016 | 0.016 | 0.0152 | YES |
| Rule 54 | 0.014 | 0.015 | 0.016 | 0.0155 | YES |
| 2D CA | 0.012 | 0.015 | 0.011 | 0.0124 | YES |
| Rule 30 | 0.013 | 0.015 | 0.012 | 0.0143 | NO |
| Rule 90 | 0.015 | 0.015 | 0.015 | 0.0141 | NO |
| Rule 150 | 0.015 | 0.015 | 0.016 | 0.0148 | NO |

**Critical Finding - All I(delta) Curves Are Flat and Overlapping**:

- No decay pattern in ANY substrate (half-life = 64 for all)
- All substrates have MI ~ 0.012-0.016 regardless of prone/resistant
- AUC = 0.33-0.67 (near random)
- Direction inverts under parameter changes

**Why Information Storage Failed**:

1. **Cell-level MI doesn't capture pattern-level structure**
   - Gliders involve coordinated spatial patterns
   - Individual cell correlations look similar across all rules

2. **Subsampling destroys spatial information**
   - Random 50-cell subsample loses pattern structure
   - Need pattern-aware measurement

3. **MI at these lags is dominated by noise floor**
   - Binary cells have limited entropy
   - Signal-to-noise ratio is poor

**Capacity Score Comparison**:

| Score Type | AUC | Separation |
|------------|-----|------------|
| Area | 0.667 | Poor |
| Half-life | 1.000* | Degenerate (all = 64) |
| Bandpass | 0.667 | Poor |

*Half-life shows AUC = 1.0 but this is degenerate - all substrates have identical half-life.

**Robustness**:
- Mean AUC: 0.46 (near random)
- Direction inverted in 5/6 conditions

**Success Criteria**:
- [FAILED] AUC >= 0.95 (actual: 0.33-0.67)
- [FAILED] No inversion (direction inverted in most conditions)
- [FAILED] Clear threshold exists (no threshold works)

**Conclusion**:

Cell-level mutual information does NOT separate prone from resistant substrates. The measurement captures noise-floor correlations, not the pattern-level structure that distinguishes glider-supporting rules from chaotic/additive ones.

**Remaining Options for Capacity Axis**:
1. Block entropy (measure information in spatial blocks)
2. Transfer entropy (directed information flow)
3. Compression ratio (algorithmic complexity)
4. Direct life-like % at low depth as the pre-screen itself

---

### Phase 14: Compression Ratio as Capacity Axis
**Status**: Complete

**Goal**: Test whether algorithmic complexity (compression) separates prone from resistant substrates.

**Hypothesis**: Additive (low) < Prone (middle) < Chaotic (high) on the complexity spectrum.

**Result - STRONG SUCCESS with Inverted Interpretation**:

| Substrate | Type | Bits/Cell | Prone |
|-----------|------|-----------|-------|
| Rule 110 | complex | 0.95 | YES |
| Rule 54 | complex | 0.88 | YES |
| 2D CA | complex | 0.51 | YES |
| Rule 30 | chaotic | 1.33 | NO |
| Rule 90 | additive | 1.33 | NO |
| Rule 150 | additive | 1.33 | NO |

**PERFECT SEPARATION - Zero Overlap**:
- Prone max: 0.95 bits/cell
- Resistant min: 1.33 bits/cell
- Gap: 0.38 bits/cell
- Classification accuracy: **100%** with threshold 1.1

**Robustness - AUC = 1.000 Across ALL Conditions**:

| Condition | AUC | Direction |
|-----------|-----|-----------|
| p=0.2 | 1.000 | Prone < Resistant |
| p=0.5 | 1.000 | Prone < Resistant |
| p=0.8 | 1.000 | Prone < Resistant |
| T=100 | 1.000 | Prone < Resistant |
| T=200 | 1.000 | Prone < Resistant |
| T=500 | 1.000 | Prone < Resistant |

**Key Insight - Interpretation Inverted from Hypothesis**:

- **Expected**: Additive < Prone < Chaotic (prone at "edge of chaos")
- **Observed**: Prone < Additive = Chaotic (prone most ordered!)

This reveals that:
1. **Resistant substrates are ALL near-random** (high entropy, ~1.33 bits/cell)
   - Rule 30 (chaotic): produces pseudorandom output
   - Rule 90, 150 (additive): also produce high-entropy XOR patterns
2. **Prone substrates have STRUCTURE** (low entropy, 0.5-0.95 bits/cell)
   - Gliders, blinkers, patterns compress well
   - Structure = life-like potential

**Depth Effect**:
All substrates converge toward low compression at high depth (more frozen = more compressible).
Prone substrates start and stay more compressible.

**Success Criteria**:
- [STRONG SUCCESS] AUC = 1.000 across all parameter variations
- [CONFIRMED] No sign inversion (direction stable: prone < resistant)
- [CONFIRMED] Clear threshold: bits/cell < 1.1 = PRONE, >= 1.1 = RESISTANT
- [REVISED] Interpretation: prone = structured (low entropy), not "edge of chaos"

**Pre-Screening Protocol**:
```
1. Run substrate at d=1 for T=200 steps
2. Compress spacetime diagram with gzip (level 9)
3. Compute: bits_per_cell = compressed_bits / (W x T)
4. IF bits_per_cell < 1.1: Substrate is PRONE
   -> Proceed to two-point calibration
   IF bits_per_cell >= 1.1: Substrate is RESISTANT
   -> Stickiness alone won't induce life-like behavior
```

**Two-Axis Framework COMPLETE**:
- **Axis 1 (Leakiness/Lyapunov)**: Controls HOW MUCH stickiness (d*)
- **Axis 2 (Compressibility)**: Predicts WHETHER stickiness will work

This metric is robust because it's scale-invariant and parameter-free.

---

## Current State

### Deliverables
- `leakiness_final.py` - Final 4-metric analysis code
- `leakiness_figure.png/pdf` - Publication figure
- `RESULTS_SUMMARY.md` - Summary of leakiness findings
- `contraction_investigation.py` - Can substrates be made contractive?
- `contraction_investigation.png` - Contraction results figure
- `selective_damping_investigation.py` - Stickiness mechanism investigation
- `selective_damping_results.png` - Selective damping results figure
- `temporal_filter_characterization.py` - Confirmation depth sweep analysis
- `temporal_filter_characterization.png/pdf` - Depth vs dynamics, filter signature
- `run_length_distributions.png` - Run length histograms by depth
- `optimal_depth_prediction.py` - Control law derivation across substrate panel
- `optimal_depth_prediction.png/pdf` - Phase diagram and gamma consistency figure
- `gamma_prediction.py` - Can gamma be predicted from baseline properties?
- `gamma_prediction.png/pdf` - Two-point validation and correlation analysis
- `end_to_end_validation.py` - Full protocol validation
- `validation_per_substrate.png/pdf` - Life-like curves with d* marked
- `validation_pooled.png/pdf` - Pooled validation and diminishing returns
- `prescreening_metric.py` - Pre-screening metric investigation
- `prescreening_metric.png/pdf` - Metric comparison and separation plots
- `motif_robustness.py` - Robustness validation of motif density
- `motif_robustness.png/pdf` - Parameter sensitivity analysis
- `information_storage.py` - Information storage as capacity axis
- `information_storage.png/pdf` - I(delta) curves and two-axis plot
- `compression_capacity.py` - Compression ratio as capacity axis
- `compression_capacity.png/pdf` - Compression distributions and two-axis plot
- `generalization_validation.py` - Phase 15-16 initial validation (compression only)
- `generalization_validation_v2.py` - Phase 15-16 two-criterion classifier
- `generalization_validation.png/pdf` - Initial validation results
- `generalization_validation_v2.png/pdf` - Two-criterion classifier results
- `PROGRESS.md` - This file

### Key Conclusions

1. **Leakiness predicts life-like behavior** (R^2 = 0.956, rho = -1.0)

2. **Lyapunov growth rate dominates** - temporal perturbation dynamics is the primary predictor

3. **Contraction is achievable but costly** - majority voting achieves negative Lyapunov but kills activity

4. **Stickiness works via temporal filtering** - not spatial selectivity, but confirmation-based inertia

5. **The sweet spot is near-zero Lyapunov** - just constrained enough to hold patterns, not so much that dynamics die

6. **Confirmation depth is a tunable filter cutoff** - acceptance ratio ~ 1/d, providing a quantitative policy dial

7. **Attempt rate is invariant to depth** - the rule's "desire" to change is constant; only execution is filtered

8. **Optimal depth scales predictably with baseline Lyapunov** - power-law model L(d) = L_min + (L_0-L_min)*d^(-gamma) fits well (R^2 > 0.96)

9. **Gamma is NOT a universal constant** - varies from 0.1 to 5.0 across substrates, requiring substrate-specific calibration

10. **Control law exists but requires calibration** - d* = ((L_0-L_min)/(L_crit-L_min))^(1/gamma) with mean prediction error of 1.35 depth units

11. **Gamma cannot be predicted from baseline properties** - Escape dimensions, branching, and activity all fail (R^2 < 0.2)

12. **Two-point calibration is sufficient** - Measure Lyapunov at d=1 and d=4, estimate gamma with r = 0.996 accuracy

13. **Substrates split into life-like-prone vs resistant** - Some substrates (110, 54, 2D) easily become life-like; others (30, 90, 150) never do

14. **Control law predicts Lyapunov threshold, not life-like onset** - Necessary but not sufficient condition; prescriptive for prone substrates

15. **Saturation pattern confirmed** - Life-like saturates at/before d*, activity continues falling (diminishing returns past d*)

16. ~~Pre-screening metric found~~ **REVISED**: Motif density is parameter-sensitive; AUC = 1.0 was artifact of specific window size

17. **Counter-intuitive insight** - Prone substrates have FEWER recurring motifs (novel dynamics), resistant have MORE (repetitive chaos) - BUT direction inverts with window size

18. **Two-axis framework partially validated** - Axis 1 (Leakiness) predicts d*, Axis 2 (Capacity) exists but no robust metric found

19. **Motif density requires careful calibration** - Use window >= 3x20, T <= 200 for reliable separation; metric direction inverts with small windows

20. **Cell-level MI does NOT separate prone/resistant** - All substrates show flat I(delta) curves around 0.012-0.016

21. ~~COMPRESSION RATIO IS THE CAPACITY AXIS~~ **REVISED**: Compression alone achieves AUC = 1.0 only on biased sample; requires activity filter for generalization

22. **Prone = Structured (compressible), Resistant = Random (incompressible)** - Inverted from "edge of chaos" hypothesis

23. **Two-criterion classifier required** - Activity filter (>1% OR Lyapunov>0) + Compression filter (<1.1 bits/cell) achieves 86.7% accuracy on expanded 50-rule sample

24. **Class I (dead) rules are a distinct failure mode** - Maximally compressible but zero life-like potential; must be filtered by activity

25. **Compression measurement is robust** - Compressor agreement r > 0.98 (gzip, bz2, lzma); representation stability r > 0.83

26. **Framework generalizes with caveats** - 86.7% accuracy, 0% FNR, 16.7% FPR on expanded set; edge cases exist

### Open Questions

1. ~~Can the temporal filtering insight be generalized to other substrates?~~ **Answered: Yes, it's a general temporal filter**
2. ~~What is the optimal confirmation depth for different substrates?~~ **Answered: d* = ((L_0-L_min)/(L_crit-L_min))^(1/gamma)**
3. Does the sigmoid model generalize to hybrid/engineered substrates?
4. Can we predict the activity-Lyapunov tradeoff curve analytically?
5. ~~Can we derive optimal depth from substrate's baseline Lyapunov?~~ **Answered: Yes, but requires substrate-specific gamma**
6. What is the relationship between filter cutoff and life-like % directly?
7. ~~Can gamma be predicted from substrate properties without fitting?~~ **Answered: No, but two-point calibration works (r=0.996)**
8. Why does Rule 54 show non-monotonic Lyapunov decay?
9. Why does 2D CA behave differently from 1D ECAs?
10. What physical property of substrates determines gamma?
11. Can the two-point protocol be simplified to a single measurement plus substrate class?
12. ~~What distinguishes life-like-prone from life-like-resistant substrates?~~ **Answered: Motif density (low = prone, high = resistant)**
13. Can resistant substrates be made prone through rule modifications?
14. ~~Is there a pre-screening metric to identify prone vs resistant substrates?~~ **Answered: Motif Density < 0.03**
15. Why do prone substrates have lower motif density? (Hypothesis: gliders are unique, not recurring) - **Confirmed but window-dependent**
16. ~~Can the pre-screening be done with fewer trials/steps?~~ **Answered: Yes, T=100-200 works, but window size is critical**
17. Is there a more robust pre-screening metric than motif density?
18. ~~Can information storage (MI) serve as a robust second axis?~~ **Answered: No, cell-level MI doesn't separate**
19. Why does motif density direction invert with window size?
20. ~~Would block entropy or transfer entropy work better than cell-level MI?~~ **Answered: Compression works perfectly (AUC=1.0)**
21. Is direct life-like % at low depth the simplest pre-screen? (Compression is simpler and robust)
22. ~~Can compression ratio capture pattern complexity?~~ **Answered: YES, perfectly separates prone/resistant**
23. ~~Why are all resistant substrates equally incompressible (~1.33 bits/cell)?~~ **Answered: Near-random output = maximum entropy**
24. ~~Can compression + Lyapunov predict life-like % quantitatively?~~ **Partially answered: Two-criterion classifier (activity + compression) achieves 86.7% accuracy**
25. **NEW**: Why do some low-compression active rules (243, 93) fail to become life-like?
26. **NEW**: Can the 50% life-like threshold be refined for better precision?

---

### Phase 15-16: Generalization and Measurement Validation
**Status**: Complete

**Goal**: Stress-test the two-axis framework on an expanded, less curated sample of 50 ECA rules.

**Phase 15: Generalization Test**

Sample: 50 ECAs (40 random + 10 known exemplars spanning Wolfram classes I-IV)

**Critical Discovery - Class I Dead Rules**:

Initial compression-only classifier failed (AUC = 0.545, Accuracy = 57.1%) because:
- Class I rules (0, 8, 128, 251, 253) die to uniform states
- Uniform states are maximally compressible (~0.02 bits/cell)
- BUT they have ZERO life-like potential (they're dead!)
- The original 6 test substrates excluded dead rules, creating bias

**Solution - Two-Criterion Classifier**:

Both criteria are NECESSARY for "prone" classification:
1. **Activity criterion**: activity > 1% OR Lyapunov > 0 (not dead)
2. **Compression criterion**: bits/cell < 1.1 (structured, not chaotic)

**Results with Two-Criterion Classifier**:

| Metric | Compression Only | Two-Criterion |
|--------|-----------------|---------------|
| Accuracy | 57.1% | **86.7%** |
| AUC (all) | 0.545 | N/A |
| AUC (active only) | N/A | **0.944** |
| False Positive Rate | 45.5% | 16.7% |
| False Negative Rate | 33.3% | **0.0%** |

**Classification by Wolfram Class**:

| Class | Description | n Validated | Accuracy |
|-------|-------------|-------------|----------|
| I | Uniform/dead | 4 | 100% |
| II | Periodic | 2 | 100% |
| III | Chaotic | 4 | 100% |
| IV | Complex | 1 | 100% |

**Failure Analysis** (2 false positives):
- Rule 243: Low compression (0.10), active, but only 40% life-like
- Rule 93: Low compression (0.05), positive Lyapunov, but only 13.3% life-like

These edge cases suggest the 50% life-like threshold may be too strict, or additional factors beyond compression+activity affect life-like emergence.

**Phase 16: Measurement Sanity Checks**

**Compressor Variation**:

| Compressor | Correlation with gzip |
|------------|----------------------|
| bz2 | r = 0.998 |
| lzma | r = 0.981 |

[STRONG SUCCESS] All compressors agree on ordering.

**Representation Variation**:

| Representation | Rank Correlation (rho) |
|----------------|------------------------|
| raw/row (baseline) | 1.000 |
| packed/row | 0.886 |
| raw/col | 0.943 |
| no transient | 0.829 |

[GOOD] Ordering mostly preserved across representations.

**Width Variation**:

| Comparison | Correlation |
|------------|-------------|
| W=64 vs W=128 | 0.981 |
| W=64 vs W=256 | 0.686 |
| W=128 vs W=256 | 0.804 |

[PARTIAL] Some width sensitivity, especially at extreme sizes. Recommendation: use consistent width (100-128).

**Success Criteria**:
- [STRONG SUCCESS] Accuracy >= 85% (actual: 86.7%)
- [PARTIAL] FPR < 15% (actual: 16.7%, just over threshold)
- [CONFIRMED] FNR < 15% (actual: 0.0%)
- [STRONG SUCCESS] Compressor correlation > 0.95 (actual: 0.981+)
- [PARTIAL] Width-invariant for reasonable sizes (r > 0.8 for W=128 vs 256)

**Revised Protocol**:

```
Given a new substrate at d=1:

1. Measure ACTIVITY (fraction of cells changing per step)
   - If activity <= 1% AND Lyapunov <= 0: RESISTANT (dead/frozen)
   - Continue to step 2 only if active

2. Measure COMPRESSION (bits per cell via gzip)
   - If bits/cell >= 1.1: RESISTANT (chaotic)
   - If bits/cell < 1.1: PRONE (structured + active)

3. For PRONE substrates:
   - Run two-point calibration (L0, L4) to predict d*
   - Apply stickiness depth d* for life-like behavior

Decision Tree:
                    [Substrate]
                         |
                   Active? (act>1% OR L>0)
                    /         \
                  NO           YES
                   |            |
           RESISTANT       Compression < 1.1?
            (dead)          /         \
                          YES          NO
                           |            |
                        PRONE       RESISTANT
                      (proceed)     (chaotic)
```

**Key Conclusions**:
- The original AUC = 1.0 on 6 substrates was partially an artifact of biased sampling
- Dead rules (Class I) require explicit activity filtering
- With two-criterion classifier, framework achieves 86.7% accuracy on expanded set
- Compression measurement is robust across compressors and representations
- Some width sensitivity exists; use consistent sizing

---

## Change Log

| Date | Phase | Key Changes |
|------|-------|-------------|
| Session 1 | 1-6 | Initial analysis through selective damping investigation |
| Session 1 | 7 | Temporal filter characterization - confirmation depth sweep |
| Session 2 | 8 | Optimal depth prediction - control law derivation |
| Session 2 | 9 | Gamma prediction - two-point calibration validated |
| Session 2 | 10 | End-to-end validation - prone vs resistant substrates discovered |
| Session 2 | 11 | Pre-screening metric - motif density separates classes (inverted) |
| Session 2 | 12 | Robustness validation - motif density is parameter-sensitive (NEGATIVE) |
| Session 2 | 13 | Information storage - cell-level MI doesn't separate (NEGATIVE) |
| Session 2 | 14 | Compression ratio - perfect separation AUC=1.0 (STRONG SUCCESS) |
| Session 2 | 15-16 | Generalization validation - two-criterion classifier, 86.7% accuracy |
| Session 2 | 17 | Paper manuscript and repository structure complete |

---

### Phase 17: Paper and Repository
**Status**: Complete

Created complete publication-ready manuscript and GitHub repository structure:

**PAPER/ Directory Contents**:
- `manuscript.md` - Full paper in Markdown (7 sections, ~4000 words)
- `manuscript.tex` - Full paper in LaTeX format
- `README.md` - GitHub-ready overview with protocol diagram
- `figures/` - 6 publication figures
- `data/` - 3 CSV files (substrate metrics, depth sweeps, validation)
- `supplementary/` - Extended methods, all rules table, negative results
- `code/protocol_implementation.py` - Reference implementation

**Paper Structure**:
1. Introduction - Two-axis framework motivation
2. Methods - Substrate definitions, metrics, protocols
3. Results - Leakiness prediction, temporal filtering, calibration, compression
4. The Complete Protocol - Decision tree, measurement budget
5. Discussion - Why it works, what compression captures, implications
6. Limitations - Edge cases, irreducible properties
7. Conclusion - Summary of validated framework

---

*Last updated: Phase 17 completion (Paper and Repository Structure)*
