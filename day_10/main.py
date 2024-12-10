
def main():
    grid = create_grid(load_input())

    # Search for the zeroes
    p2_sum = 0
    for x, row in enumerate(grid):
        for y, col in enumerate(row):
            if col == 0:
                search_sum = search_path(x, y, grid)
                print(f'Trailhead at {x}, {y} has a rating of {search_sum}')
                p2_sum += search_sum

    print(f'P2: {p2_sum}')

def search_path(x, y, grid):
    out = 0
    current_digit = 0
    path = [[(x, y)]]

    while True:
        # Search for next digit for each coord in last path element
        search_coords = path[-1]
        found_coords = []
        for coord in search_coords:
            found = search_digit(coord[0], coord[1], current_digit+1, grid)
            found_coords += found
        path.append(list(set(found_coords)))

        if current_digit == 8: # Exit Condition
            out = len(path[-1])
            break
        
        current_digit += 1

    # Search for trails
    trails = [[(x, y)]]

    # Loop through all steps starting at 1
    for step in path[1:]:

        # Loop through all trails
        starting_trail_len = len(trails)
        for trail_idx in range(starting_trail_len):
            trail = trails[trail_idx]

            # Get a copy of the trail
            trail_copy = trail.copy()

            # Get the last trail coordinate
            last_trail_coord = trail[-1]
            added_flag = False

            # Loop through the coords in the step
            for step_coord in step:

                # Check if the step_coord is aligned with the last trail coord
                if is_trail_aligned(last_trail_coord, step_coord):

                    if added_flag is False: # Add the step to the existing trail if not already done
                        trail.append(step_coord)
                        added_flag = True
                    else: # Register a new trail with the step coord at the end
                        new_trail = trail_copy.copy()
                        new_trail.append(step_coord)
                        trails.append(new_trail)


    # Count the trails that have a length of 10
    count = 0
    for trail in trails:
        if len(trail) == 10:
            count += 1
    
    return count

def is_trail_aligned(coord_1, coord_2):
    flag = False
    x_dis = coord_1[0] - coord_2[0]
    y_dis = coord_1[1] - coord_2[1]
    if (x_dis == 1 or x_dis == -1) and y_dis == 0:
        flag = True
    elif (y_dis == 1 or y_dis == -1) and x_dis == 0:
        flag = True
    return flag


def search_digit(x, y, search_digit, grid):
    out = []
    search_coords = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1)
    ]

    for coord in search_coords:
        if coord[0] >= 0 and coord[1] >= 0 and coord[0] < len(grid) and coord[1] < len(grid[0]):
            if grid[coord[0]][coord[1]] == search_digit:
                out.append(coord)

    return out

def visualize_grid(grid):
    for row in grid:
        print(''.join([f'{x}' for x in row]))

def create_grid(data):
    grid = []
    for line in data:
        line = line.strip()
        row = []
        for char in line:
            row.append(int(char))
        grid.append(row)
    return grid

def load_input():
    with open('input.1.txt', 'r') as f:
        data = f.readlines()
    return data

main()