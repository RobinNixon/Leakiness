# Figure Captions

## Figure 1: Leakiness vs Life-Like Percentage

**File:** `fig1_leakiness_vs_lifelike.png`

**Caption:** Relationship between weighted leakiness score and life-like percentage across five substrate types. The sigmoid fit (R² = 0.96) captures a phase transition around L = 0.39: substrates below this threshold achieve high life-like rates, while substrates above it are increasingly constrained. Perfect rank correlation (ρ = -1.0) demonstrates that leakiness reliably predicts life-like potential.

---

## Figure 2: Temporal Filter Signature

**File:** `fig2_temporal_filter_signature.png`

**Caption:** Evidence that stickiness operates as a temporal low-pass filter. (a) Acceptance ratio scales as 1/d, characteristic of temporal filtering. (b) Comparison with spatial consensus shows stickiness preserves 20× more activity at equivalent Lyapunov reduction. The temporal filtering mechanism blocks transient fluctuations while preserving sustained dynamics.

---

## Figure 3: Depth Prediction via Power-Law Decay

**File:** `fig3_depth_prediction.png`

**Caption:** Power-law relationship between Lyapunov exponent and confirmation depth. (a) Lyapunov decay follows L(d) = L_min + (L₀ - L_min)·d^(-γ) with substrate-specific decay exponent γ. (b) The control law d* = ((L₀ - L_min)/(L_crit - L_min))^(1/γ) accurately predicts optimal depth. (c) Two-point gamma estimation (using d=1 and d=4) achieves r = 0.996 correlation with full-fit gamma.

---

## Figure 4: Two-Axis Framework

**File:** `fig4_two_axis_framework.png`

**Caption:** The two-axis framework for predicting life-like behavior. Horizontal axis: Lyapunov (leakiness component) determines HOW MUCH filtering is needed. Vertical axis: Compression (capacity) determines WHETHER filtering will succeed. Substrates in the lower-left quadrant (low leakiness, low compression) are life-like-prone; substrates in the upper-right are resistant.

---

## Figure 5: Generalization Validation

**File:** `fig5_generalization_validation.png`

**Caption:** Validation of the two-criterion classifier on 50 ECA rules. (a) Classification matrix showing PRONE vs RESISTANT predictions against observed life-like outcomes. (b) The two-criterion classifier (activity gate + compression threshold) achieves 86.7% accuracy and AUC = 0.944 on active rules, with 0% false negative rate.

---

## Figure 6: Pooled Validation Results

**File:** `fig6_validation_pooled.png`

**Caption:** Pooled validation results showing the relationship between predicted and observed life-like behavior across all validation substrates. The strong agreement demonstrates that the two-axis framework generalizes beyond the original training set to accurately predict life-like potential for arbitrary discrete substrates.

---

## Summary Table

| Figure | Title | Key Message |
|--------|-------|-------------|
| 1 | Leakiness vs Life-Like | R² = 0.96 prediction, phase transition at L = 0.39 |
| 2 | Temporal Filter | Stickiness is temporal filtering, not spatial |
| 3 | Depth Prediction | Two-point calibration achieves r = 0.996 |
| 4 | Two-Axis Framework | Leakiness + Capacity predict life-like potential |
| 5 | Generalization | 86.7% accuracy, AUC = 0.944 on 50 rules |
| 6 | Pooled Validation | Framework generalizes to new substrates |
