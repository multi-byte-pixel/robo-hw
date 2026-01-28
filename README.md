# Bayesian Belief & Noisy Sensing — Robot Movement Simulator

Background

Bayesian thinking frames uncertainty as degrees of belief rather than single-point answers. Start with a prior belief about a quantity, incorporate evidence via a likelihood model, and compute a posterior belief by applying Bayes' rule. Repeated observations or noisy sensors shift the posterior: a stronger, more informative likelihood moves belief more; noisy, ambiguous evidence keeps beliefs diffuse.

Key concepts:
- Prior: initial probability distribution over states before new evidence.
- Likelihood: probability of observed evidence given each possible state (sensor model).
- Posterior: updated belief after combining prior and likelihood.
- Belief distribution: a full probability distribution representing uncertainty over states.

How this relates to the simulator

The simulator in `robot_sim.py` models a small, one-dimensional robot moving from position 0 to a boundary at position 3. Squares alternate between `window` and `wall`. The robot samples an intended step size from {1,2,3} with a base distribution (0.2, 0.7, 0.1). However, the robot's perception of each square is noisy: windows and walls can be misidentified with configurable probabilities.

Rather than explicitly running a Bayes update step each time, the program simulates many trials of the robot's stochastic behavior (movement sampling + noisy perception). Aggregating the final positions across trials yields an empirical distribution over final positions — this distribution approximates the posterior probability over final positions given the probabilistic movement model and the sensor noise. In Bayesian terms:

- The movement and sensor models define a generative model (prior over action outcomes and likelihood of perceived sensor readings).
- Each simulated trial is a sampled execution from the generative model.
- The histogram of final positions across many trials is an empirical belief (posterior-like) about where the robot ends up after N steps.

What the code implements (`robot_sim.py`)

- Movement sampling: default probabilities {1:0.2, 2:0.7, 3:0.1}.
- Alternating square labels: position 0 is `window`, 1 is `wall`, 2 is `window`, etc.
- Noisy perception: configurable `p_correct_wall` and `p_correct_window` control the probability the true label is perceived correctly.
- Collision/stop behavior: if the robot perceives a `wall` along its intended path it stops before that perceived wall.
- Multi-trial simulation: run many trials and compute the probability mass function over final positions.
- Plotting: saves or shows a bar chart of final-position probabilities.

How this embodies Bayesian ideas

- Sensor noise is encoded as a likelihood: P(perceived | true state).
- By sampling many trials and aggregating outcomes, the program builds an empirical belief distribution over final positions that reflects both action stochasticity and sensor uncertainty.
- You can experiment with priors/likelihoods by changing movement probabilities or perception accuracies and observing the resulting change in the empirical distribution.

Quick start

Requirements:
- Python 3.8+ (3.10/3.11 recommended)
- `matplotlib` (for plotting)

Install dependencies (if needed):

```bash
pip install matplotlib
```

Run the simulator (example):

```bash
python robot_sim.py --steps 5 --trials 20000 --seed 1
```

Save the plot to `out.png`:

```bash
python robot_sim.py --steps 5 --trials 20000 --seed 1 --save out.png
```

Files

- `robot_sim.py` — main simulator (see [robot_sim.py](robot_sim.py)).
- `README.md` — this document (see [README.md](README.md)).

Suggested experiments

- Vary `--trials` to improve the empirical estimate (more trials → smoother distribution).
- Modify the movement probabilities in `RobotSimulator` to reflect different action priors.
- Change `p_correct_wall` and `p_correct_window` when constructing `RobotSimulator` to see how sensor fidelity shifts the final-position distribution.
