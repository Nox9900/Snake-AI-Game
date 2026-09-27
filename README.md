# Snake AI Game

A Snake game played by a reinforcement-learning agent. The agent learns from
rewards alone, with no hard-coded rules: it starts out moving almost randomly
and gradually improves at avoiding walls, its own body, and steering toward
food.

The approach is **Deep Q-Learning (DQN)** built with PyTorch.

## How it works

Each move the agent observes the board, picks one of three actions, and receives
a reward. It stores the experience in a replay buffer and trains a small neural
network to estimate which action is best from each state.

### State (11 inputs)

The agent sees danger relative to its current heading, plus where the food is:

| Index | Meaning |
| --- | --- |
| 0 | Collision if moving straight |
| 1 | Collision if turning right |
| 2 | Collision if turning left |
| 3 | Currently moving left |
| 4 | Currently moving right |
| 5 | Currently moving up |
| 6 | Currently moving down |
| 7 | Food is to the left |
| 8 | Food is to the right |
| 9 | Food is above |
| 10 | Food is below |

### Actions (3 outputs)

`[1,0,0]` straight, `[0,1,0]` turn right, `[0,0,1]` turn left.

### Rewards

| Event | Reward |
| --- | --- |
| Eats food | `+10` |
| Dies (wall, self, or timeout) | `-10` |
| Anything else | `0` |

### Network

A single hidden layer is used for this state :

```
Linear(11, 256) -> ReLU -> Linear(256, 3)
```

### Training

- **Optimizer:** Adam, `lr=0.001`
- **Discount factor:** `gamma=0.9`
- **Replay buffer:** 100,000 transitions
- **Batch size:** 1,000 (sampled once per finished game)
- **Exploration:** `epsilon = 80 - n_games`, so the agent explores randomly for
  roughly the first 80 games and then plays greedily
- **Loss:** MSE against the Q-learning target
  `r + gamma * max(Q(s'))`, using `r` alone on the terminal step

Two updates happen per step: `train_short_memory` fits the current transition
immediately, and `train_long_memory` replays a random batch once a game ends.

The best model so far is saved to `Model/model.pth` whenever the score beats the
record.

## Requirements

- Python 3.10+
- The packages in `requirements.txt`

## Installation

```bash
pip install -r requirements.txt
```

Note: the requirement is `pygame-ce`, not `pygame`. It is the maintained fork
and it still installs the `pygame` module the code imports, so no import changes
are needed.

## Usage

```bash
python main.py
```

A window opens showing the agent training. Scores and the running mean are
plotted after every game.

Training is deliberately endless, so **score and mean score are expected to
climb for several hundred games** before the agent looks competent. Stop it
with `Ctrl+C`.

## Project structure

```
Snake AI Game/
├── main.py              # training loop
├── requirements.txt
├── Game/
│   ├── __init__.py
│   ├── game.py          # SnakeGame, Direction, Point, collision + rendering
│   ├── agent.py         # state extraction, replay buffer, action selection
│   └── helper.py        # live matplotlib plot
└── Model/
    ├── __init__.py
    ├── model.py         # Linear_QNet and QTrainner
    └── model.pth        # best model (created on first record)
```

[//]: # (## Notes)

[//]: # ()
[//]: # (- `Linear_QNet.save&#40;&#41;` anchors the path to `Model/model.py` rather than the)

[//]: # (  working directory, so saving works regardless of where you run from.)

[//]: # (- `model.pth` and `__pycache__/` are generated at runtime. They are currently)

[//]: # (  untracked rather than ignored, so they will show up in `git status`; add a)

[//]: # (  `.gitignore` if that is noisy. Delete `model.pth` to start training from a)

[//]: # (  fresh network.)

[//]: # (- Speed is capped at 40 FPS by `Game.SPEED`, so a long training run is)

[//]: # (  wall-clock bound as much as it is compute bound. Raising `SPEED` in)

[//]: # (  `Game/game.py` trains faster at the cost of a harder-to-watch window.)
