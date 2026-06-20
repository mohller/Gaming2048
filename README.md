# Gaming2048

A Python framework for simulating and recording games of 2048, with a step interface designed for ML training.

## Tile encoding

Tiles are stored as log₂ values: the tile `2` is stored as `1`, `4` as `2`, `8` as `3`, and so on. This keeps values small and uniform.

## Code structure

### Code usage

```python
from source import collapse, operate, pop_next, is_game_over
```

| Function | Description |
|---|---|
| `collapse(elements)` | Merges a single compacted row/column according to 2048 rules |
| `operate(grid, direction)` | Applies a swipe (0=up, 1=right, 2=down, 3=left) to a grid |
| `pop_next(grid)` | Places a new tile (value `1`) in a random empty cell |
| `is_game_over(grid)` | Returns `True` when the board is full and no move is possible |

### Move generation and replay

```python
from source import generate_game, playback
```

`generate_game(dim)` runs a full random episode on a `dim×dim` board and returns `(initial, moves, pops)` — the starting grid, the sequence of moves taken, and where each new tile appeared.

`playback(initial, moves, pops, moments=None)` replays those records and returns a list of grid snapshots at the requested move indices. Defaults to the final state.

### Step interface

```python
from source import step

new_grid, reward, done, valid = step(grid, direction)
```

- `valid` — `False` if the move produced no change (illegal move)
- `reward` — increase in total board value (log₂ scale) from the merge
- `done` — `True` when the game is over

## Quickstart

```python
import numpy as np
from source import pop_next, step, is_game_over

grid = pop_next(np.zeros((4, 4)))

while not is_game_over(grid):
    direction = np.random.choice(4)
    grid, reward, done, valid = step(grid, direction)
```

See `testing.ipynb` for batch simulation and statistics on random-player performance.

## Dependencies

- `numpy`
- `matplotlib` (notebook only)
