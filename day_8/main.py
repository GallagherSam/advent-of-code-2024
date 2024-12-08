
def main():
    # Load the file
    lines = load_input()

    # Cast to a grid
    grid = generate_grid(lines)

    # Find all antinode locations
    antinode_locations = []
    for x, y, signal in next_dish(grid):
        print('\nNext Dish.')
        print(x, y, signal)
        
        # Find the compatible dishes
        for n_x, n_y, n_item in search_dish(signal, x, y, grid):
            print(n_x, n_y, n_item)

            # Find all of the antinodes
            antinode_locations += get_antinodes(x, y, n_x, n_y, grid)

    print(antinode_locations)

    # Add dish location for anitnodes
    for x, row in enumerate(grid):
        for y, char in enumerate(row):
            if char != '.':
                antinode_locations.append((x, y))

    # Get unique locations
    antinode_locations = list(set(antinode_locations))

    # Make sure both points are gtr than 0 and within bounds
    antinode_locations = [x for x in antinode_locations if (x[0] >=0 and x[1] >= 0) and (x[0] < len(grid) and x[1] < len(grid[0]))]

    # Filter out dish locations
    print(f'There are {len(antinode_locations)} unique antinodes.')

    visualize(grid, antinode_locations)

def filter_dishes(locations, grid):
    out = []
    for loc in locations:
        if grid[loc[0]][loc[1]] == '.':
            out.append(loc)
    return out

# Updated for part 2
def get_antinodes(x_1, y_1, x_2, y_2, grid):
    out = []
    # Get just the antinodes that (x_1, y_2) create from (x_2, y_2)
    distance = (
        x_1 - x_2,
        y_1 - y_2
    )

    while True:
        next_node = (
            distance[0] + x_1,
            distance[1] + y_1
        )

        if (next_node[0] >= 0 and next_node[1] >= 0) and (next_node[0] < len(grid) and next_node[1] < len(grid[1])):
            out.append(next_node)
            x_1 = next_node[0]
            y_1 = next_node[1]
        else:
            break

    return out

def search_dish(signal, s_x, s_y, grid):
    for x, row in enumerate(grid):
        for y, item in enumerate(row):

            # Skipping search dish
            if x == s_x and y == s_y:
                continue

            if item == signal:
                yield (x, y, item)
    

def next_dish(grid):
    for x, row in enumerate(grid):
        for y, item in enumerate(row):
            if item != '.':
                yield (x, y, item)


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
    with open('input.1.txt', 'r') as f:
        data = f.readlines()
    return data

def visualize(grid, locations):
    for x, row in enumerate(grid):
        string = ''
        for y, char in enumerate(row):
            flag = False
            for loc in locations:
                if x == loc[0] and y == loc[1]:
                    string += '#'
                    flag = True
                    break
            if flag is False:
                string += char
        print(string)
            

main()