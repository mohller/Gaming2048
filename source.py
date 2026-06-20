import numpy as np

def collapse(elements):
    """Takes a column/row of values and collapse them
    """
    out, skip = [], False
    for k in range(len(elements)):
        if skip:
            skip = False
            continue
        if k + 1 < len(elements) and elements[k] == elements[k + 1]:
            out.append(elements[k] + 1)
            skip = True
        else:
            out.append(elements[k])
    return out

def operate(grid, direction=0):
    """Performs the operations resulting from swiping in the game.
       The grid contains the content of the game previous to the action
       and the direction is a value from 0-3 representing a swipe in
       the corresponding directions [up, right, down, left].
    """
    dim = grid.shape[0]

    if direction in [0, 2]:
        grid = grid.T

    new_lines = [collapse([val for val in line if val]) for line in grid]

    grid = np.zeros_like(grid)

    for k, row in enumerate(new_lines):
        if direction in [0, 3]:
            grid[k, :len(row)] = row
        else:
            grid[k, dim - len(row):] = row

    if direction in [0, 2]:
        grid = grid.T

    return grid
    
def is_game_over(grid):
    """Returns True when the grid is full and no move changes it.
    """
    if np.any(grid == 0):
        return False
    return all(np.all(operate(grid, d) == grid) for d in range(4))

def pop_next(grid):
    """Adds a new element of lowest value in a random 
       position, and modifies the grid to include it.
    """
    r, c = np.where(grid == 0)
    random_idx = np.random.choice(len(r))

    out = grid.copy()
    out[r[random_idx], c[random_idx]] = 1

    return out

def generate_game(dim):
    """Generate an entire gameplay
    """
    grid = pop_next(np.zeros((dim, dim)))
    initial = grid.copy()

    moves, pops = [], []
    while not is_game_over(grid):
        nextgrid = grid.copy()
        while np.all(nextgrid == grid):
            dir = np.random.choice(range(4))
            nextgrid = operate(grid, dir)

        grid = nextgrid
        moves.append(dir)
        
        grid = pop_next(grid)
        pops.append(np.hstack(np.where(grid != nextgrid)))

    pops = np.vstack(pops)

    return initial, moves, pops

def playback(initial, moves, pops, moments=None):
    """Returns the status of the grid for the given moments.
    """
    grid = initial.copy()

    if moments is None:
        moments = [len(moves) - 1]

    snapshots = []
    for k, (m, idcs) in enumerate(zip(moves, pops)):
        grid = operate(grid, m)
        grid[idcs[0], idcs[1]] = 1

        if k in moments:
            snapshots.append(grid)

    return snapshots

def step(grid, direction):
    """Apply one move and return (new_grid, reward, done, valid).

    valid=False when the direction produced no change (illegal move).
    reward is the increase in total tile value (log2 scale).
    done=True when no further moves are possible.
    """
    new_grid = operate(grid, direction)
    valid = not np.all(new_grid == grid)
    if valid:
        new_grid = pop_next(new_grid)
    reward = int(np.sum(new_grid) - np.sum(grid))
    done = is_game_over(new_grid)
    return new_grid, reward, done, valid