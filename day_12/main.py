
def main():
    # Get the data
    lines = load_input()
    grid = generate_grid(lines)

    # Get the sum of area and perimeter for each region
    region_sum = 0
    for x, row in enumerate(grid):
        for y, plant in enumerate(row):

            if plant != '.': # We use '.' to denote a region we've already searched
                region_sum += get_region(grid, plant, x, y)
    
    print(f'P2: {region_sum}')

def get_region(grid, plant, x, y):
    region_coords = [(x, y)]
    searched_coords = [(x, y)]

    # Start a recursive search for touching coordinates with the same plant
    search(grid, plant, x+1, y, searched_coords, region_coords)
    search(grid, plant, x-1, y, searched_coords, region_coords)
    search(grid, plant, x, y+1, searched_coords, region_coords)
    search(grid, plant, x, y-1, searched_coords, region_coords)

    # Get all unique coordinates
    region_coords = list(set(region_coords))
    # print(region_coords)
    # visualize_region(region_coords)
    # input()
    
    # Calculate the perimeter
    perimeter = calc_perimeter_p2(region_coords)

    # Update grid with '.' for found regions
    for coord in region_coords:
        grid[coord[0]][coord[1]] = '.'

    # Return the area * perimeter
    # print(plant, len(region_coords), perimeter)
    return len(region_coords) * perimeter

def search(grid, plant, x, y, search_coords, found_coords):
    # Check if this coord has already been searched
    flag = False
    for coord in search_coords:
        if coord[0] == x and coord[1] == y:
            flag = True
    if flag:
        return

    # Add this coordinate to the search coords
    search_coords.append((x, y))

    # Check the provided search coordinate for the plant
    if x >= 0 and y >= 0 and x < len(grid) and y < len(grid[0]) and grid[x][y] == plant:
        found_coords.append((x, y))
        search(grid, plant, x+1, y, search_coords, found_coords)
        search(grid, plant, x-1, y, search_coords, found_coords)
        search(grid, plant, x, y+1, search_coords, found_coords)
        search(grid, plant, x, y-1, search_coords, found_coords)

def calc_perimeter_p2(coords):
    perimeter = 0

    # Build a map of the edges for the region, borrow from p1 solution
    indv_edges = []
    for coord in coords:
        up, down, left, right = (True, True, True, True)
        for coord_s in coords:

            if coord == coord_s: # Skip Self
                continue

            if coord[0] == coord_s[0] + 1 and coord[1] == coord_s[1]: # Adjacent up
                up = False
            elif coord[0] == coord_s[0] - 1 and coord[1] == coord_s[1]: # Adjacent down
                down = False
            elif coord[0] == coord_s[0] and coord[1] == coord_s[1] + 1: # Adjacent left
                left = False
            elif coord[0] == coord_s[0] and coord[1] == coord_s[1] - 1: # Adjacent right
                right = False
        
        # Add to the edges map
        indv_edges.append({
            'x': coord[0],
            'y': coord[1],
            'up': up,
            'down': down,
            'left': left,
            'right': right
        })

    # Search through the individual edges to find edge segments
    for edge in indv_edges:

        for dir in ['up', 'down', 'left', 'right']:
            search_coords = []
            if edge[dir] is True:
                # print(indv_edges)
                # print(f'Found edge on {dir} for {edge}')
                # Increment edges and remove this edge from play
                perimeter += 1
                edge[dir] = False

                # Search for adjacent edges
                if dir == 'up' or dir == 'down':
                    search_adjacent_edges(indv_edges, dir, edge['x'], edge['y']+1, search_coords)
                    search_adjacent_edges(indv_edges, dir, edge['x'], edge['y']-1, search_coords)
                else:
                    search_adjacent_edges(indv_edges, dir, edge['x']+1, edge['y'], search_coords)
                    search_adjacent_edges(indv_edges, dir, edge['x']-1, edge['y'], search_coords)
                # print(search_coords)
                # print('post search changes')
                # print(indv_edges)
                # input()

    return perimeter
    

def search_adjacent_edges(edges, dir, x, y, searched_coords):
    # Check if we've searched this coord already
    for coord in searched_coords:
        if coord[0] == x and coord[1] == y:
            return
    searched_coords.append((x, y))
        
    # Check if a edge exists for this coordinate
    for edge in edges:
        if edge['x'] == x and edge['y'] == y and edge[dir] is True:

            # Remove the edge from the searches
            edge[dir] = False
            # print(f'found adjacent edge {edge}')

            # Trigger searching for next coords
            if dir == 'up' or dir == 'down':
                search_adjacent_edges(edges, dir, x, y+1, searched_coords)
                search_adjacent_edges(edges, dir, x, y-1, searched_coords)
            else:
                search_adjacent_edges(edges, dir, x+1, y, searched_coords)
                search_adjacent_edges(edges, dir, x-1, y, searched_coords)

def calc_perimeter(coords):
    perimeter = 0

    # Loop through the coords and check adjacency
    for coord in coords:
        up, down, left, right = (True, True, True, True)
        for coord_s in coords:

            if coord == coord_s: # Skip Self
                continue

            if coord[0] == coord_s[0] + 1 and coord[1] == coord_s[1]: # Adjacent up
                up = False
            elif coord[0] == coord_s[0] - 1 and coord[1] == coord_s[1]: # Adjacent down
                down = False
            elif coord[0] == coord_s[0] and coord[1] == coord_s[1] + 1: # Adjacent right
                right = False
            elif coord[0] == coord_s[0] and coord[1] == coord_s[1] - 1: # Adjacent left
                left = False
        
        # Increment perimeter based on true values
        if up:
            perimeter += 1
        if down:
            perimeter += 1
        if right:
            perimeter += 1
        if left:
            perimeter += 1
    
    return perimeter

def visualize_region(coords):
    out = {}
    for coord in coords:
        if coord[0] in out:
            out[coord[0]].append(coord[1])
        else:
            out[coord[0]] = [coord[1]]
    keys = sorted(out.keys())


    maxes = []
    for key in keys:
        maxes.append(max(out[key]))
    max_val = max(maxes) + 1

    top_str = "----"
    for i in range(max_val):
        top_str += f'{i}'
    print(top_str)

    for key in keys:
        region_str = f'{key} - '
        for i in range(max_val):
            if i in out[key]:
                region_str += 'X'
            else:
                region_str += '.'
        print(region_str)

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

main()