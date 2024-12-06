from copy import deepcopy

def p_2():
    data = load_input()
    grid = generate_grid(data)
    touched_spaces = []

    # Get the guard starting coordinates
    for x in range(len(grid)-1):
        for y in range(len(grid[0])-1):
            if grid[x][y] == '^':
                guard_pos = (x, y)
                starting_pos = (x, y)
                grid[x][y] = '.'
                touched_spaces.append(guard_pos)
    print(f'Guard starts at: {guard_pos}')

    # Define a callback for each tick
    def early_stopping_callback(next_pos,  next_direction, grid, touched_spaces):
        if (next_pos[0], next_pos[1], next_direction) in touched_spaces:
            return True
        return False
    
    # Start finding valid obstacles
    valid_obstacles = 0

    # We only need to search spaces the guard touches on their initial route
    touched_spaces = update_loop(grid, guard_pos, 90, touched_spaces)
    touched_spaces = list(set(touched_spaces))

    print(f'Testing {len(touched_spaces)} spaces.')
    for space in touched_spaces:
        print(f'\nTesting {space}')
        
        # Validate the space
        if space[0] == starting_pos[0] and space[1] == starting_pos[1]: # GUARD STARTING POSITION
            continue

        # Setup the test params
        test_touched_spaces = []
        guard_pos = tuple(list(starting_pos))
        guard_direction = 90
        test_grid = deepcopy(grid)
        test_grid[space[0]][space[1]] = '#'

        stopped_early = update_loop(test_grid, guard_pos, guard_direction, test_touched_spaces, save_direction=True, early_stopping_callback=early_stopping_callback)
        if stopped_early is True:
            print('Found a valid obstacle!')
            valid_obstacles += 1
        else:
            steps = len(list(set(stopped_early)))
            print(f'Guard walked {steps} with this obstacle')

    print(f'There are {valid_obstacles} valid obstacles to create a loop')


def p_1():
    data = load_input()
    grid = generate_grid(data)
    touched_spaces = []

    # Get the guard starting coordinates
    for x in range(len(grid)-1):
        for y in range(len(grid[0])-1):
            if grid[x][y] == '^':
                guard_pos = (x, y)
                grid[x][y] = '.'
                touched_spaces.append(guard_pos)
    print(f'Guard starts at: {guard_pos}')

    # Implement a game loop until the guard is out of frame
    guard_direction = 90
    touched_spaces = update_loop(grid, guard_pos, guard_direction, touched_spaces)
    touched_spaces = list(set(touched_spaces))

    print('\nOUTPUT')
    # visualize_path(grid, touched_spaces)
    print(f'The guard walked in: {len(touched_spaces)} spaces.')

def update_loop(grid, guard_pos, guard_direction, touched_spaces, save_direction=False, early_stopping_callback=None):
    stopped_early = False

    while True:
        # Get the next update
        (next_pos, next_direction, left_frame) = update(grid, guard_pos, guard_direction)

        # Check exit condition
        if left_frame:
            break

        # Check early stopping condition
        if early_stopping_callback is not None:
            if early_stopping_callback(next_pos, next_direction, grid, touched_spaces):
                # Early stopping returned true, so stop the loop
                stopped_early = True
                break
        
        if save_direction:
            touched_spaces.append((next_pos[0], next_pos[1], next_direction))
        else:
            touched_spaces.append(next_pos)
        
        guard_pos = next_pos
        guard_direction = next_direction
    
    # HATE THIS MIXED RETURN
    if stopped_early:
        return True
    else:
        return touched_spaces

def update(grid, current_guard_pos, current_guard_direction):
    # Setup return values
    next_guard_pos, next_guard_direction, left_frame = (
        (0, 0),
        -1,
        False
    )

    # Get the next position
    if current_guard_direction == 90: # UP
        next_guard_pos = (current_guard_pos[0]-1, current_guard_pos[1])
    elif current_guard_direction == 180: # LEFT
        next_guard_pos = (current_guard_pos[0], current_guard_pos[1]-1)
    elif current_guard_direction == 270: # DOWN
        next_guard_pos = (current_guard_pos[0]+1, current_guard_pos[1])
    elif current_guard_direction == 0: # RIGHT
        next_guard_pos = (current_guard_pos[0], current_guard_pos[1]+1)
    else:
        print(current_guard_direction)
        raise Exception('UNKNOWN GUARD DIRECTION')
    
    # Validate the next position
    if next_guard_pos[0] < 0 or next_guard_pos[0] >= len(grid) or next_guard_pos[1] < 0 or next_guard_pos[1] >= len(grid[0]): # OUT OF BOUNDS
        left_frame = True
        return (next_guard_pos, next_guard_direction, left_frame)
    
    elif grid[next_guard_pos[0]][next_guard_pos[1]] == '#': # OBSTACLE BLOCKING
        next_guard_direction = current_guard_direction - 90
        if next_guard_direction < 0:
            next_guard_direction = 270
        next_guard_pos = current_guard_pos
    
    else: # NOT OUT OF FRAME NOR OBSTACLE BLOCKING
        next_guard_direction = current_guard_direction
    
    return (next_guard_pos, next_guard_direction, left_frame)
        
def visualize_grid(grid, guard_pos):
    for x, line in enumerate(grid):
        string = ''
        for y, char in enumerate(line):
            if x == guard_pos[0] and y == guard_pos[1]:
                string += '^'
            else:
                string += char
        print(string)

def visualize_path(grid, path):
    for x, line in enumerate(grid):
        string = ''
        for y, char in enumerate(line):
            flag = True
            for coord in path:
                if x == coord[0] and y == coord[1]:
                    flag = False
                    string += '$'
            if flag:
                string += char
        print(string)

def generate_grid(data):
    grid = []
    for line in data:
        line = line.strip()
        grid_line = []
        for char in line:
            grid_line.append(char)
        grid.append(grid_line)
    return grid

def load_input():
    with open('input.1.txt', 'r') as f:
        data = f.readlines()
    return data

p_2()