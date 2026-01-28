# Robot movement simulator
# Models a robot moving from left (0) to right (max_pos=3).
# At each time step the robot samples an intended step size from {1,2,3}
# with probabilities (0.2, 0.7, 0.1). The robot cannot pass position 3.
# Squares alternate between "window" and "wall" (pos 0 == window).
# The robot's perception of each square is noisy; misidentifications
# can reduce the achieved movement (robot stops before perceived wall).

import random
import collections
import argparse
import matplotlib.pyplot as plt


class RobotSimulator:
    def __init__(self,
                 max_pos=3,
                 move_probs=None,
                 p_correct_wall=1.0,
                 p_correct_window=1.0,
                 rng=None):
        self.max_pos = max_pos
        # default move distribution: 0->10%, 1->70%, 2->20%
        self.move_probs = move_probs or {0:0.1, 1:0.7, 2:0.2}
        self.p_correct_wall = p_correct_wall
        self.p_correct_window = p_correct_window
        self.rng = rng or random.Random()
        # precompute cumulative distribution for sampling
        self._moves, self._cum = self._build_cdf(self.move_probs)

    def _build_cdf(self, probs_dict):
        moves = sorted(probs_dict)
        cum = []
        s = 0.0
        for m in moves:
            s += probs_dict[m]
            cum.append(s)
        return moves, cum

    def _sample_move(self):
        u = self.rng.random()
        for m, c in zip(self._moves, self._cum):
            if u <= c:
                return m
        return self._moves[-1]

    @staticmethod
    def true_label_at(pos):
        # pos 0 == window, pos1 == wall, pos2 == window, etc.
        return "window" if (pos % 2) == 0 else "wall"

    def perceive_label(self, true_label):
        # returns perceived label given the true label and confusion probabilities
        if true_label == "wall":
            if self.rng.random() <= self.p_correct_wall:
                return "wall"
            else:
                return "window"
        else:
            if self.rng.random() <= self.p_correct_window:
                return "window"
            else:
                return "wall"

    def run_single(self, n_steps, return_trace=False):
        pos = 0
        trace = []
        for step in range(n_steps):
            intended = self._sample_move()
            target = min(pos + intended, self.max_pos)
            # sense the label at the target position (for localization only)
            # walls/windows do not block movement
            true = self.true_label_at(target)
            perceived = self.perceive_label(true)
            trace.append((target, true, perceived))
            pos = target
        if return_trace:
            return pos, trace
        return pos

    def simulate(self, n_steps, trials=10000):
        counts = collections.Counter()
        for _ in range(trials):
            final = self.run_single(n_steps)
            counts[final] += 1
        # convert to probabilities
        probs = {pos: counts[pos]/trials for pos in range(self.max_pos+1)}
        return probs

    def compute_exact_posterior(self, n_steps):
        """Compute the exact distribution over final positions after n_steps
        using dynamic programming and the model's stochastic transitions.
        Returns a dict {pos: probability} for pos in 0..max_pos.
        """
        # Build transition probabilities T[pos][next_pos]
        # Robot moves from pos by sampling move distance m, arriving at min(pos + m, max_pos)
        # Sensor reading (wall/window) at target position does not affect movement
        T = {pos: {s: 0.0 for s in range(self.max_pos+1)} for pos in range(self.max_pos+1)}
        for pos in range(self.max_pos+1):
            for m, pm in self.move_probs.items():
                target = min(pos + m, self.max_pos)
                T[pos][target] += pm

        # dynamic programming over time steps
        dist = [0.0] * (self.max_pos+1)
        dist[0] = 1.0
        for _ in range(n_steps):
            new = [0.0] * (self.max_pos+1)
            for pos in range(self.max_pos+1):
                if dist[pos] == 0.0:
                    continue
                for s in range(self.max_pos+1):
                    new[s] += dist[pos] * T[pos][s]
            dist = new

        return {pos: dist[pos] for pos in range(self.max_pos+1)}


def plot_distribution(probs, n_steps, trials, move_probs=None, out_file=None):
    if move_probs is None:
        move_probs = {0:0.1, 1:0.7, 2:0.2}
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    
    # Left: input movement distribution
    move_distances = sorted(move_probs.keys())
    move_values = [move_probs[d] for d in move_distances]
    axes[0].bar(move_distances, move_values, tick_label=move_distances, color='steelblue')
    axes[0].set_xlabel('Movement distance')
    axes[0].set_ylabel('Probability')
    axes[0].set_title('Input Movement Distribution')
    axes[0].set_ylim(0, 1)
    axes[0].grid(axis='y', alpha=0.25)
    
    # Right: final position distribution
    positions = sorted(probs.keys())
    values = [probs[p] for p in positions]
    axes[1].bar(positions, values, tick_label=positions, color='coral')
    axes[1].set_xlabel('Final position')
    axes[1].set_ylabel('Probability')
    axes[1].set_title(f'Final position distribution after {n_steps} steps ({trials} trials)')
    axes[1].set_ylim(0, 1)
    axes[1].grid(axis='y', alpha=0.25)
    
    plt.tight_layout()
    if out_file:
        plt.savefig(out_file, bbox_inches='tight')
        print(f'Saved plot to {out_file}')
    else:
        plt.show()


def compare_distributions(move_probs_list, n_steps, trials=10000, use_exact=False):
    """Compare empirical or exact distributions across multiple movement probability sets.
    
    Args:
        move_probs_list: List of dicts, each containing "movement", "p_correct_wall", "p_correct_window"
        n_steps: Number of time steps to simulate
        trials: Number of simulation trials (ignored if use_exact=True)
        use_exact: If True, compute exact posteriors; if False, run simulations
    """
    num_dists = len(move_probs_list)
    fig, axes = plt.subplots(2, num_dists, figsize=(4*num_dists, 7))
    
    for idx, dist_config in enumerate(move_probs_list):
        move_probs = dist_config["movement"]
        p_correct_wall = dist_config.get("p_correct_wall", 1.0)
        p_correct_window = dist_config.get("p_correct_window", 1.0)
        
        sim = RobotSimulator(move_probs=move_probs, 
                           p_correct_wall=p_correct_wall,
                           p_correct_window=p_correct_window)
        
        if use_exact:
            probs = sim.compute_exact_posterior(n_steps)
            title_suffix = "exact"
        else:
            probs = sim.simulate(n_steps, trials=trials)
            title_suffix = f"empirical ({trials} trials)"
        
        positions = sorted(probs.keys())
        values = [probs[p] for p in positions]
        
        # Top row: input movement distribution (blue)
        move_distances = sorted(move_probs.keys())
        move_values = [move_probs[d] for d in move_distances]
        axes[0, idx].bar(move_distances, move_values, tick_label=move_distances, color='steelblue')
        axes[0, idx].set_xlabel('Movement distance')
        axes[0, idx].set_ylabel('Probability')
        axes[0, idx].set_title(f"Dist {idx+1} Input Distribution")
        axes[0, idx].set_ylim(0, 1)
        axes[0, idx].grid(axis='y', alpha=0.25)
        
        # Bottom row: final position distribution (orange)
        axes[1, idx].bar(positions, values, tick_label=positions, color='coral')
        axes[1, idx].set_xlabel('Final position')
        axes[1, idx].set_ylabel('Probability')
        axes[1, idx].set_title(f"Dist {idx+1} Final Positions ({title_suffix})")
        axes[1, idx].set_ylim(0, 1)
        axes[1, idx].grid(axis='y', alpha=0.25)
    
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Simulate robot movement with noisy sensing.')
    parser.add_argument('--steps', type=int, default=5, help='Number of time steps')
    parser.add_argument('--trials', type=int, default=20000, help='Number of simulation trials')
    parser.add_argument('--seed', type=int, default=1, help='RNG seed')
    parser.add_argument('--save', type=str, default=None, help='Optional output PNG filename')
    parser.add_argument('--compare', action='store_true', help='Compare all 6 distributions from movement_table')
    parser.add_argument('--exact', action='store_true', help='Use exact posteriors instead of simulation')
    args = parser.parse_args()

    if args.compare:
        # Import movement distributions from movement_table
        from movement_table import distribution_sets
        compare_distributions(distribution_sets, args.steps, trials=args.trials, use_exact=args.exact)
    else:
        sim = RobotSimulator(rng=random.Random(args.seed))
        probs = sim.simulate(args.steps, trials=args.trials)

        print('Final position probabilities:')
        for p in range(sim.max_pos+1):
            print(f'  pos {p}: {probs.get(p,0):.4f}')

        plot_distribution(probs, args.steps, args.trials, move_probs=sim.move_probs, out_file=args.save)


if __name__ == '__main__':
    main()
