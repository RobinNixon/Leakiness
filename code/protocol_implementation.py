"""
Reference Implementation: Life-Like Prediction Protocol

This module implements the complete two-axis framework for predicting
life-like behavior in Elementary Cellular Automata (ECA).

Usage:
    from protocol_implementation import predict_lifelike

    result = predict_lifelike(rule=110)
    print(f"Classification: {result['classification']}")
    print(f"Optimal depth: {result['d_star']}")

Author: Robin Nixon
"""

import numpy as np
import gzip
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class PredictionResult:
    """Result of life-like prediction protocol."""
    rule: int
    classification: str  # 'prone', 'resistant_dead', 'resistant_chaotic'
    compression: float
    activity: float
    lyapunov_d1: float
    lyapunov_d4: Optional[float]
    gamma: Optional[float]
    d_star: Optional[float]
    expected_lifelike: str  # 'high', 'low', 'none'


class StickyECA:
    """
    1D Elementary Cellular Automaton with stickiness (temporal bit inertia).

    Parameters
    ----------
    size : int
        Number of cells in the automaton.
    rule : int
        Wolfram rule number (0-255).
    depth : int
        Confirmation depth (number of consecutive timesteps required
        for a state change to execute).
    """

    def __init__(self, size: int = 100, rule: int = 110, depth: int = 1):
        self.size = size
        self.rule = rule
        self.depth = depth
        self.rule_table = self._make_rule_table(rule)
        self.counters = None

    def _make_rule_table(self, rule: int) -> dict:
        """Create lookup table for ECA rule."""
        return {
            tuple(map(int, format(i, '03b'))): (rule >> i) & 1
            for i in range(8)
        }

    def random_state(self, p: float = 0.5) -> np.ndarray:
        """Generate random initial state."""
        state = (np.random.random(self.size) < p).astype(int)
        self.counters = np.zeros(self.size, dtype=int)
        return state

    def get_rule_output(self, state: np.ndarray) -> np.ndarray:
        """Compute what the rule wants (before stickiness)."""
        new_state = np.zeros_like(state)
        for i in range(self.size):
            left = state[(i - 1) % self.size]
            center = state[i]
            right = state[(i + 1) % self.size]
            new_state[i] = self.rule_table[(left, center, right)]
        return new_state

    def step(self, state: np.ndarray) -> np.ndarray:
        """Execute one timestep with stickiness."""
        if self.counters is None:
            self.counters = np.zeros(self.size, dtype=int)

        rule_wants = self.get_rule_output(state)
        wants_change = rule_wants != state

        # Increment counters where rule wants change, reset otherwise
        self.counters = np.where(wants_change, self.counters + 1, 0)

        # Execute only if counter reaches confirmation depth
        execute = self.counters >= self.depth
        new_state = np.where(execute, rule_wants, state)
        self.counters = np.where(execute, 0, self.counters)

        return new_state


def measure_compression(
    substrate: StickyECA,
    n_steps: int = 200,
    n_seeds: int = 20,
    transient: int = 50
) -> float:
    """
    Measure compression ratio (bits per cell) of spacetime diagrams.

    Parameters
    ----------
    substrate : StickyECA
        The substrate to measure.
    n_steps : int
        Number of timesteps to record.
    n_seeds : int
        Number of random initializations to average.
    transient : int
        Steps to skip before recording.

    Returns
    -------
    float
        Mean bits per cell across seeds.
    """
    bits_per_cell_list = []

    for _ in range(n_seeds):
        state = substrate.random_state(p=0.5)

        # Skip transient
        for _ in range(transient):
            state = substrate.step(state)

        # Collect spacetime diagram
        spacetime = []
        for _ in range(n_steps):
            state = substrate.step(state)
            spacetime.append(state.copy())

        spacetime = np.array(spacetime, dtype=np.uint8)

        # Compress and measure
        raw_bytes = spacetime.tobytes()
        compressed = gzip.compress(raw_bytes, compresslevel=9)

        n_cells = spacetime.size
        bits_per_cell = (len(compressed) * 8) / n_cells
        bits_per_cell_list.append(bits_per_cell)

    return np.mean(bits_per_cell_list)


def measure_activity(
    substrate: StickyECA,
    n_trials: int = 15,
    n_steps: int = 50,
    warmup: int = 50
) -> float:
    """
    Measure fraction of cells that change per step.

    Returns
    -------
    float
        Mean activity rate (0 to 1).
    """
    activities = []

    for _ in range(n_trials):
        state = substrate.random_state()

        # Warmup
        for _ in range(warmup):
            state = substrate.step(state)

        trial_activity = []
        for _ in range(n_steps):
            new_state = substrate.step(state)
            activity = np.mean(state != new_state)
            trial_activity.append(activity)
            state = new_state

        activities.append(np.mean(trial_activity))

    return np.mean(activities)


def measure_lyapunov(
    substrate: StickyECA,
    n_trials: int = 20,
    n_steps: int = 20,
    warmup: int = 20
) -> float:
    """
    Measure Lyapunov-like growth rate.

    Returns
    -------
    float
        Mean log-growth rate of perturbation.
    """
    growth_rates = []

    for _ in range(n_trials):
        state = substrate.random_state()

        # Warmup
        for _ in range(warmup):
            state = substrate.step(state)

        # Create perturbed copy with separate substrate
        pert_substrate = StickyECA(
            size=substrate.size,
            rule=substrate.rule,
            depth=substrate.depth
        )
        pert_substrate.random_state()
        if substrate.counters is not None:
            pert_substrate.counters = substrate.counters.copy()

        pert_state = state.copy()
        idx = np.random.randint(len(pert_state))
        pert_state[idx] = 1 - pert_state[idx]

        orig_state = state.copy()

        # Evolve both trajectories
        for _ in range(n_steps):
            orig_state = substrate.step(orig_state)
            pert_state = pert_substrate.step(pert_state)

        # Compute growth rate
        final_diff = np.sum(orig_state != pert_state)
        if final_diff > 0:
            growth_rate = np.log(final_diff) / n_steps
            growth_rates.append(growth_rate)

    return np.mean(growth_rates) if growth_rates else -0.1


def classify_substrate(
    compression: float,
    activity: float,
    lyapunov: float,
    compression_threshold: float = 1.1,
    activity_threshold: float = 0.01
) -> str:
    """
    Two-criterion classifier for prone vs resistant.

    Parameters
    ----------
    compression : float
        Bits per cell from compression measurement.
    activity : float
        Activity rate (0 to 1).
    lyapunov : float
        Lyapunov-like growth rate.
    compression_threshold : float
        Threshold for structured vs chaotic (default 1.1).
    activity_threshold : float
        Threshold for active vs dead (default 0.01).

    Returns
    -------
    str
        'prone', 'resistant_dead', or 'resistant_chaotic'
    """
    is_active = activity > activity_threshold or lyapunov > 0
    is_structured = compression < compression_threshold

    if not is_active:
        return 'resistant_dead'
    elif not is_structured:
        return 'resistant_chaotic'
    else:
        return 'prone'


def two_point_calibration(
    rule: int,
    size: int = 100,
    L_min: float = -0.05,
    L_crit: float = 0.05
) -> Dict[str, float]:
    """
    Execute two-point calibration to predict optimal depth.

    Parameters
    ----------
    rule : int
        Wolfram rule number.
    size : int
        Automaton size.
    L_min : float
        Asymptotic minimum Lyapunov (default -0.05).
    L_crit : float
        Critical Lyapunov threshold (default 0.05).

    Returns
    -------
    dict
        Contains L0, L4, gamma, d_star
    """
    # Measure Lyapunov at d=1
    sub_d1 = StickyECA(size=size, rule=rule, depth=1)
    L0 = measure_lyapunov(sub_d1)

    # Measure Lyapunov at d=4
    sub_d4 = StickyECA(size=size, rule=rule, depth=4)
    L4 = measure_lyapunov(sub_d4)

    # Estimate gamma
    numerator = L0 - L_min
    denominator = L4 - L_min

    if denominator <= 0 or numerator <= 0 or numerator <= denominator:
        gamma = 0.3  # Default fallback
    else:
        gamma = np.log(numerator / denominator) / np.log(4)
        gamma = max(0.01, min(gamma, 5.0))  # Bound gamma

    # Predict optimal depth
    if L0 <= L_crit:
        d_star = 1.0
    else:
        ratio = (L0 - L_min) / (L_crit - L_min)
        if ratio > 0 and gamma > 0:
            d_star = ratio ** (1 / gamma)
            d_star = max(1.0, min(d_star, 20.0))
        else:
            d_star = 8.0  # Fallback

    return {
        'L0': L0,
        'L4': L4,
        'gamma': gamma,
        'd_star': d_star
    }


def predict_lifelike(
    rule: int,
    size: int = 100,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Execute complete life-like prediction protocol.

    This is the main entry point for the framework.

    Parameters
    ----------
    rule : int
        Wolfram rule number (0-255).
    size : int
        Automaton size.
    verbose : bool
        Print progress messages.

    Returns
    -------
    dict
        Complete prediction results including classification,
        metrics, and optimal depth (if prone).

    Example
    -------
    >>> result = predict_lifelike(rule=110)
    >>> print(f"Rule 110: {result['classification']}, d*={result['d_star']}")
    """
    if verbose:
        print(f"Analyzing Rule {rule}...")

    # Step 1: Measure at d=1
    substrate = StickyECA(size=size, rule=rule, depth=1)

    if verbose:
        print("  Measuring compression...")
    compression = measure_compression(substrate)

    if verbose:
        print("  Measuring activity...")
    activity = measure_activity(substrate)

    if verbose:
        print("  Measuring Lyapunov (d=1)...")
    lyapunov_d1 = measure_lyapunov(substrate)

    # Step 2: Classify
    classification = classify_substrate(compression, activity, lyapunov_d1)

    if verbose:
        print(f"  Classification: {classification}")

    # Step 3: For prone substrates, run two-point calibration
    lyapunov_d4 = None
    gamma = None
    d_star = None
    expected_lifelike = 'none'

    if classification == 'prone':
        if verbose:
            print("  Running two-point calibration...")

        sub_d4 = StickyECA(size=size, rule=rule, depth=4)
        lyapunov_d4 = measure_lyapunov(sub_d4)

        cal = two_point_calibration(rule, size)
        gamma = cal['gamma']
        d_star = cal['d_star']

        expected_lifelike = 'high'

        if verbose:
            print(f"  gamma = {gamma:.3f}")
            print(f"  d* = {d_star:.1f}")
    elif classification == 'resistant_dead':
        expected_lifelike = 'none'
    else:  # resistant_chaotic
        expected_lifelike = 'low'

    result = {
        'rule': rule,
        'classification': classification,
        'compression': compression,
        'activity': activity,
        'lyapunov_d1': lyapunov_d1,
        'lyapunov_d4': lyapunov_d4,
        'gamma': gamma,
        'd_star': d_star,
        'expected_lifelike': expected_lifelike
    }

    if verbose:
        print(f"  Expected life-like: {expected_lifelike}")
        print("  Done.")

    return result


def batch_analyze(rules: list, size: int = 100) -> list:
    """
    Analyze multiple rules.

    Parameters
    ----------
    rules : list
        List of rule numbers to analyze.
    size : int
        Automaton size.

    Returns
    -------
    list
        List of prediction results.
    """
    results = []
    for rule in rules:
        result = predict_lifelike(rule, size, verbose=False)
        results.append(result)
        print(f"Rule {rule}: {result['classification']}")
    return results


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        rule = int(sys.argv[1])
        result = predict_lifelike(rule)
    else:
        # Demo: analyze a few representative rules
        print("=" * 60)
        print("Life-Like Prediction Protocol - Demo")
        print("=" * 60)

        demo_rules = [0, 30, 90, 110, 150]
        print(f"\nAnalyzing demo rules: {demo_rules}\n")

        for rule in demo_rules:
            result = predict_lifelike(rule)
            print()

        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print("""
Classification Guide:
  - prone: Substrate supports life-like behavior with stickiness
  - resistant_dead: Substrate dies to uniform state (Class I)
  - resistant_chaotic: Substrate too chaotic for coherent patterns

For prone substrates, apply confirmation depth d* for optimal life-like behavior.
""")
