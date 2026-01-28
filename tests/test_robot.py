import pytest
import types
import copy

from robot_sim import RobotSimulator, compare_distributions
import movement_table
import matplotlib.pyplot as plt


def test_build_cdf_and_sample_move_deterministic():
    rng = random = __import__("random").Random(0)
    # deterministic move_probs: always move 2
    sim = RobotSimulator(move_probs={2: 1.0}, rng=rng)
    # after one step should be at position 2 (max_pos default 3)
    pos = sim.run_single(1)
    assert pos == 2
    # after two steps should be at position 3 (bounded by max_pos)
    pos = sim.run_single(2)
    assert pos == 3


def test_simulate_probability_sum():
    sim = RobotSimulator(move_probs={0:0.1,1:0.7,2:0.2})
    probs = sim.simulate(3, trials=1000)
    # probabilities over positions 0..max_pos should sum to ~1
    total = sum(probs.values())
    assert abs(total - 1.0) < 1e-6


def test_compute_exact_equals_simulation_for_deterministic():
    # deterministic movement: always move 1
    sim = RobotSimulator(move_probs={1: 1.0})
    exact = sim.compute_exact_posterior(3)
    empirical = sim.simulate(3, trials=1000)
    # For deterministic moves, empirical should match exact (positions deterministic)
    for pos in range(sim.max_pos+1):
        assert abs(exact.get(pos, 0.0) - empirical.get(pos, 0.0)) < 1e-6


def test_movement_table_schema():
    # verify movement_table has expected structure
    for i, cfg in enumerate(movement_table.distribution_sets, 1):
        assert isinstance(cfg, dict)
        assert "movement" in cfg
        assert isinstance(cfg["movement"], dict)
        # probabilities should sum to ~1
        total = sum(cfg["movement"].values())
        assert abs(total - 1.0) < 1e-9
        # sensor params present and between 0 and 1
        assert 0.0 <= cfg.get("p_correct_wall", 1.0) <= 1.0
        assert 0.0 <= cfg.get("p_correct_window", 1.0) <= 1.0


def test_compare_distributions_functional(monkeypatch):
    # Prevent plots from showing by monkeypatching plt.show
    monkeypatch.setattr(plt, "show", lambda: None)
    # call compare_distributions with exact=True to avoid long simulations
    compare_distributions(movement_table.distribution_sets, n_steps=3, trials=10, use_exact=True)
    # If it returns without raising, consider the functional test passed

