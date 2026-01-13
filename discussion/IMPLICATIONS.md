# Implications of the Leakiness Framework

## For Artificial Life Engineering

### The Standard Approach (Challenged)
Traditional artificial life research often involves:
- Trial and error with many parameter combinations
- Intuitive rule design based on "edge of chaos" heuristics
- No principled way to predict success

### The New Approach
The two-axis framework provides a **predictive engineering protocol**:

1. **Pre-screen** substrates with activity and compression
2. **Classify** as PRONE or RESISTANT
3. **Calibrate** with two Lyapunov measurements
4. **Apply** predicted confirmation depth

**Result:** Life-like behavior emerges predictably from substrate properties.

## For Understanding Self-Maintenance

### Key Insight: Temporal Filtering
Stickiness works as a **temporal low-pass filter**, not spatial selective damping:
- Blocks transient fluctuations (noise)
- Preserves sustained dynamics (signal)
- Acceptance ratio scales as 1/d

This explains why simple confirmation mechanisms enable complex self-maintenance.

### Leakiness as Fundamental Property
A substrate's intrinsic tendency to amplify or suppress perturbations (Lyapunov) is the primary determinant of life-like potential.

```
TIGHT VESSELS (low leakiness)     LOOSE VESSELS (high leakiness)
         |                                   |
Perturbations CONTRACT            Perturbations EXPAND
         |                                   |
     Life-like                           Resistant
```

## For Complexity Science

### Inversion of "Edge of Chaos"
Prone substrates are MORE structured (lower compression), not at intermediate complexity. This inverts the edge-of-chaos expectation.

### Orthogonality of Computation and Life-Like
- Rule 110: Turing-complete AND life-like-prone
- Rule 30: Cryptographically random AND life-like-resistant

Computational power and self-maintenance are orthogonal properties.

## For Physical Substrates

### Natural Analogs
Physical systems with built-in temporal filtering:
- Neural refractory periods
- Chemical activation barriers
- Thermal hysteresis

These natural "stickiness" mechanisms may explain why biological substrates support life-like behavior.

### Design Principles
To engineer self-maintaining systems:
1. Choose substrates with low intrinsic leakiness
2. Or add temporal filtering to high-leakiness substrates
3. Ensure sufficient structural capacity (low compression)
