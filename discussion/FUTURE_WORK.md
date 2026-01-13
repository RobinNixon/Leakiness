# Future Work and Open Problems

## Theoretical Extensions

### 1. Continuous Substrates
Can the leakiness framework extend to:
- Continuous state spaces?
- Differential equations?
- Neural networks?

**Challenge:** Defining discrete "confirmation depth" in continuous settings.

### 2. Gamma as Irreducible Property
The filter efficiency exponent γ remains substrate-specific and must be calibrated empirically. Can we predict γ from structural properties?

### 3. Edge Cases
Rules 243 and 93 suggest gradient rather than hard boundary between prone and resistant. What determines borderline cases?

## Empirical Extensions

### 1. Higher-Dimensional Systems
Test framework on:
- 3D cellular automata
- Graph-structured substrates
- Spatially irregular lattices

### 2. Alternative Filtering Mechanisms
Compare stickiness (confirmation) with:
- Refractory periods
- Spatial consensus
- Probabilistic thresholds

### 3. Biological Validation
Test predictions on:
- Neural network simulations with refractory periods
- Chemical reaction networks
- Ecological models

## Protocol Refinements

### 1. Multi-Point Calibration
Would 3+ Lyapunov measurements improve γ estimation beyond r = 0.996?

### 2. Dynamic Depth Adjustment
Can optimal depth be adjusted dynamically based on local dynamics?

### 3. Compression Alternatives
Are there better capacity metrics than LZ77 compression ratio?

## Open Questions

1. **Why does temporal filtering preserve structure?** What is the information-theoretic basis?

2. **Is there a universal optimal filter?** Or is substrate-specific calibration always necessary?

3. **What determines γ?** Can filter efficiency be predicted from rule structure?

4. **Can resistant substrates become prone?** Through mechanisms other than stickiness?

5. **What is the relationship to thermodynamics?** Is there an entropic cost to temporal filtering?
