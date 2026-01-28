# Robot Simulator — Usage Guide

## Quick Start

Run the simulator with defaults:
```bash
python robot_sim.py
```

This runs a single simulation with the default movement distribution and plots the input distribution alongside the resulting final positions.

## Command-Line Options

### Basic Usage

```bash
python robot_sim.py [OPTIONS]
```

### Options

#### `--steps N`
Number of time steps the robot will take. Each step, the robot samples a movement distance (0, 1, or 2) and attempts to move that far right.
- **Default:** 5
- **Example:** `python robot_sim.py --steps 10`

#### `--trials N`
Number of simulation trials to run (only used with `--compare` or without `--exact`).
- **Default:** 20000
- **Example:** `python robot_sim.py --trials 5000`

#### `--seed N`
Random seed for reproducibility.
- **Default:** 1
- **Example:** `python robot_sim.py --seed 42`

#### `--save FILENAME`
Save the output plot to a PNG file instead of displaying it.
- **Default:** None (displays plot interactively)
- **Example:** `python robot_sim.py --save output.png`

#### `--compare`
Compare all 6 movement distributions from `movement_table.py` side-by-side. Shows the input distribution (top) and resulting final positions (bottom) for each.
- **Default:** False
- **Example:** `python robot_sim.py --compare --steps 5`

#### `--exact`
Compute exact posterior distributions using dynamic programming instead of running empirical simulations. Much faster for exact results.
- **Default:** False (runs empirical simulation)
- **Example:** `python robot_sim.py --exact --steps 3`
- **Note:** Ignored when not using `--compare`

## Common Usage Examples

### Single run with default settings
```bash
python robot_sim.py
```
Shows input distribution and final positions after 5 steps, using 20,000 trials.

### Compare all 6 distributions with exact computation
```bash
python robot_sim.py --compare --steps 5 --exact
```
Displays all 6 movement distributions side-by-side with their exact final-position posteriors. No simulation, pure calculation.

### Single run with more steps
```bash
python robot_sim.py --steps 10 --trials 10000
```
Simulates the robot taking 10 steps, using 10,000 trials for better statistical accuracy.

### Save a comparison plot
```bash
python robot_sim.py --compare --steps 7 --exact --save comparison.png
```
Computes exact posteriors for all 6 distributions after 7 steps and saves the result to `comparison.png`.

### Reproducible run
```bash
python robot_sim.py --seed 123 --steps 5 --trials 5000
```
Uses a fixed random seed for reproducible results.

## What the Output Shows

### Single Run (default)
- **Left panel (blue):** Input movement distribution — probability of moving 0, 1, or 2 steps.
- **Right panel (orange):** Final position distribution — where the robot ends up after N steps.

### Compare Mode (`--compare`)
- **Top row (blue bars):** Input movement distributions for each of the 6 scenarios.
- **Bottom row (orange bars):** Resulting final-position distributions.

## Movement Distributions

The 6 distributions in `movement_table.py` represent different movement behaviors:
1. **Dist 1:** Favors no movement (0 at 70%)
2. **Dist 2:** Favors small movement (1 at 70%)
3. **Dist 3:** Favors larger movement (2 at 70%)
4-6. **Dist 4-6:** Alternative allocations of (0.1, 0.2, 0.7)

Each distribution can have different sensor accuracy parameters (`p_correct_wall`, `p_correct_window`).

## Exact vs. Empirical

- **Empirical** (default): Runs many simulation trials and estimates probabilities from the results.
  - More realistic, accounts for randomness.
  - Takes longer.
  - Probabilities are approximate.

- **Exact** (`--exact`): Computes the true posterior analytically using dynamic programming.
  - Instantaneous (no simulation overhead).
  - True mathematical result.
  - Allows validation of empirical results.
