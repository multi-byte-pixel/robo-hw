# All 6 possible permutations of the movement probabilities (0.1, 0.7, 0.2)
# Each distribution includes:
#   - movement: dict mapping distance (0, 1, or 2) to its probability
#   - p_correct_wall: probability sensor correctly identifies a wall (default 1.0 = always correct)
#   - p_correct_window: probability sensor correctly identifies a window (default 1.0 = always correct)

distribution_sets = [
    {
        "movement": {0: 0.7, 1: 0.2, 2: 0.1},
        "p_correct_wall": 1.0,
        "p_correct_window": 1.0,
    },  # Dist 1: favors no movement (distance 0)
    {
        "movement": {0: 0.2, 1: 0.7, 2: 0.1},
        "p_correct_wall": 1.0,
        "p_correct_window": 1.0,
    },  # Dist 2: favors distance 1
    {
        "movement": {0: 0.2, 1: 0.1, 2: 0.7},
        "p_correct_wall": 1.0,
        "p_correct_window": 1.0,
    },  # Dist 3: favors distance 2
    {
        "movement": {0: 0.7, 1: 0.1, 2: 0.2},
        "p_correct_wall": 1.0,
        "p_correct_window": 1.0,
    },  # Dist 4: favors no movement (different allocation)
    {
        "movement": {0: 0.1, 1: 0.2, 2: 0.7},
        "p_correct_wall": 1.0,
        "p_correct_window": 1.0,
    },  # Dist 5: favors distance 2 (different allocation)
    {
        "movement": {0: 0.1, 1: 0.7, 2: 0.2},
        "p_correct_wall": 1.0,
        "p_correct_window": 1.0,
    },  # Dist 6 (default): favors distance 1 (different allocation)
]

# Example usage:
# You can iterate over these distributions to simulate or plot comparisons.
if __name__ == "__main__":
    print("All 6 Movement Distributions:")
    for i, dist in enumerate(distribution_sets, 1):
        print(f"Distribution {i}: {dist}")