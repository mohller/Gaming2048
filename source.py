import numpy as np

def collapse(elements):
    """Takes a column/row of values and collapse them
    """
    merge_points = [elements[k] == elements[k+1] for k in range(len(elements) - 1)] + [False, ]
    keep = [False, ] + merge_points[:-1]

    if np.any(merge_points):
        out = [el+1 if match else el for el, match in zip(elements, merge_points)]
        out = [el for el, kp in zip(out, keep) if not kp]
    else:
        out = elements
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
    while np.any(grid == 0):
        nextgrid = grid.copy()
        while np.all(nextgrid == grid):
            dir = np.random.choice(range(4))
            nextgrid = operate(grid, dir)
        
        grid = nextgrid.copy()
        moves.append(dir)
        
        grid = pop_next(grid)
        pops.append(np.hstack(np.where(grid != nextgrid)))

    pops = np.vstack(pops)

    return initial, moves, pops

def playback(initial, moves, pops, moments=[-1]):
    """Returns the status of the grid for the given moments.
    """
    grid = initial.copy()

    if moments == [-1]:
        moments = [len(moves) - 1]

    snapshots = []
    for k, (m, idcs) in enumerate(zip(moves, pops)):
        grid = operate(grid, m)
        grid[idcs[0], idcs[1]] = 1

        if k in moments:
            snapshots.append(grid)

    return snapshots