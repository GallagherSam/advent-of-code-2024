
# Globals
ROTATE_SCORE = 1000
MOVE_SCORE = 1

def main():
    lines = load_input()
    grid = generate_grid(lines)

    # Get the starting position of the reindeer
    starting_pos = get_starting_pos(grid)

    # Iterate all of the possible paths, calculating their score as we move
    paths = [
        {
            'score': 0,
            'path': [starting_pos],
            'facing': 'right',
            'active': True
        }
    ]
    while True:
        new_paths = []
        for path in paths:
            current_pos = path['path'][-1]
            print(f'Looking at curren pos of {current_pos}')

            # Check if the path splits into a few options
            split_pos = check_split(grid, current_pos)
            if len(split_pos) > 0:

                valid_splits = []
                for split in split_pos:

                    # Make sure the split isn't already in our path
                    if split in path['path']:
                        continue

                    # Spot check for dead ends
                    if check_deadend(grid, split, (split[0] - current_pos[0], split[1] - current_pos[1])):
                        continue
                    else:
                        valid_splits.append(split)
                
                if len(valid_splits) >= 1: # There are paths to follow, add one to the next in the path and then create more paths
                    add_to_path(path, valid_splits[0])
                    for split in valid_splits[1:]:
                        create_new_path(new_paths, path, split)
                
                else: # There are no valid splits, this path is dead
                    path['active'] = False
            
        # Add the new paths to paths
        paths += new_paths

def create_new_path(paths, current_path, coord):
    pass

def add_to_path(path, coord):
    pass

def check_deadend(grid, pos, dir):
    print('check deadend')
    print(pos)
    # We want to look along this path to see if it either a) reaches the end of b) hits any splits. If not, it's a dead end
    flag = True
    while True:

        if grid[pos[0]][pos[1]] == '#': # Check if we hit a wall - denoting a dead end
            break

        if grid[pos[0]][pos[1]] == 'E': # Check for the end - we can stop this loop
            flag = False
            break

        splits = check_split(grid, pos)
        if len(splits) > 2: # There are valid splits ahead, we can stop the loop
            print('splits')
            print(splits)
            flag = False
            break

        # Increment the pos in the dir
        pos = (pos[0] + dir[0], pos[1] + dir[1])
        print(f'next pos {pos}')
    return flag
        
        

def check_split(grid, pos):
    top, down, left, right = [
        (pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0], pos[1] + 1)
    ]

    splits = []
    for dir in [top, down, left, right]:
        if dir[0] >= 0 and dir[0] < len(grid) and dir[1] >= 0 and dir[1] < len(grid[0]):
            dir_pos = grid[dir[0]][dir[1]]
            if dir_pos == '.' or dir_pos == 'E':
                splits.append(dir)
    return splits

def get_starting_pos(grid):
    starting_pos = None
    for top, row in enumerate(grid):
        for right, char in enumerate(row):
            if char == 'S':
                starting_pos = (top, right)
    return starting_pos

def generate_grid(lines):
    grid = []
    for line in lines:
        line = line.strip()
        row = []
        for char in line:
            row.append(char)
        grid.append(row)
    return grid


def load_input():
    with open('input.2.txt', 'r') as f:
        lines = f.readlines()
    return lines

main()