# Extended Methodology

## Substrate Implementations

### Binary 1D Elementary Cellular Automata (ECA)

The canonical 256 Wolfram rules operating on binary states with 3-cell neighborhoods. Each rule is specified by an 8-bit lookup table:

```python
def _make_rule_table(self, rule):
    return {
        tuple(map(int, format(i, '03b'))): (rule >> i) & 1
        for i in range(8)
    }
```

Key rules investigated:
- **Rule 110**: Class IV complex, proven Turing-complete
- **Rule 30**: Class III chaotic, used in cryptographic RNG
- **Rule 90**: Class III additive, XOR-based
- **Rule 54**: Class IV complex
- **Rule 150**: Class III additive

### Binary 2D Cellular Automata

Conway's Game of Life on a 20×20 toroidal grid:
- Birth: exactly 3 neighbors
- Survival: 2 or 3 neighbors
- Death: otherwise

### Stickiness Mechanism

Each cell maintains a counter tracking consecutive timesteps where the rule requests a state change:

```python
def step(self, state):
    rule_wants = self.get_rule_output(state)
    wants_change = rule_wants != state

    self.counters = np.where(wants_change, self.counters + 1, 0)
    execute = self.counters >= self.depth

    new_state = np.where(execute, rule_wants, state)
    self.counters = np.where(execute, 0, self.counters)

    return new_state
```

## Measurement Protocols

### Lyapunov-like Growth Rate

1. Initialize random state
2. Warmup: 20 steps
3. Create perturbed copy (flip single random cell)
4. Evolve both trajectories for N=20 steps
5. Compute: L = log(Hamming distance) / N
6. Repeat 30 trials, report mean

### Compression Ratio

1. Initialize random state (p=0.5)
2. Remove transient: 50 steps
3. Collect spacetime diagram: 200 steps × width
4. Serialize as raw bytes (one byte per cell)
5. Compress with gzip level 9
6. Compute: bits_per_cell = (compressed_size × 8) / total_cells
7. Repeat 20 seeds, report mean

### Life-Like Classification

A trial is classified as life-like if:
1. **Activity persists**: mean(changes per step) > 0.1%
2. **Activity bounded**: mean(changes per step) < 80%
3. **Activity stable**: variance(changes) < 0.1
4. **Structure present**: |spatial_autocorr - 0.5| × 2 > 0.1

## Parameter Sensitivity Analysis

### Compression Robustness

| Variation | Correlation with Baseline |
|-----------|---------------------------|
| gzip vs bz2 | r = 0.998 |
| gzip vs lzma | r = 0.981 |
| Raw vs packed bytes | rho = 0.886 |
| Row-major vs column-major | rho = 0.943 |
| With vs without transient removal | rho = 0.829 |
| W=64 vs W=128 | r = 0.981 |
| W=128 vs W=256 | r = 0.804 |

### Life-Like Classification Sensitivity

| Parameter | Effect |
|-----------|--------|
| Warmup steps (20-100) | Minimal effect on classification |
| Evaluation steps (50-200) | Stable above 50 steps |
| Activity threshold (0.1%-1%) | Affects edge cases only |
| Structure threshold (0.05-0.15) | Moderate sensitivity |

## Statistical Methods

### AUC Calculation

Using Mann-Whitney U statistic:
```python
def compute_auc(prone_values, resistant_values):
    count = 0
    for p in prone_values:
        for r in resistant_values:
            if p < r:  # prone should have lower compression
                count += 1
            elif p == r:
                count += 0.5
    return count / (len(prone_values) * len(resistant_values))
```

### Bootstrap Confidence Intervals

500 bootstrap samples with replacement, reporting 2.5th and 97.5th percentiles.

### Two-Criterion Classification

Both criteria required for "prone":
1. Activity > 1% OR Lyapunov > 0
2. Compression < 1.1 bits/cell

This addresses the Class I (dead rule) problem where maximally compressible states have zero life-like potential.
