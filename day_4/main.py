def load_input():
    with open('input.1.txt', 'r') as f:
        data = f.readlines()
    return data

def main():
    data = load_input()

    count = 0
    for x, line in enumerate(data):
        for y, char in enumerate(line):

            # A marks the spot this time
            if char == 'A':
                count += x_search(x, y, data)
    
    print(count)

def x_search(x, y, data):
    corners = [
        (x - 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y - 1),
        (x + 1, y + 1)
    ]

    # Edge detection
    if corners[0][0] < 0 or corners[0][1] < 0 or corners[3][0] >= len(data) or corners[3][1] >= len(data[1]):
        return 0

    if corner_check(corners[0], corners[3], data) and corner_check(corners[1], corners[2], data):
        return 1
    
    return 0

def corner_check(c_1, c_2, data):
    if data[c_1[0]][c_1[1]] == "M":
        if data[c_2[0]][c_2[1]] == "S":
            return True
    elif data[c_1[0]][c_1[1]] == "S":
        if data[c_2[0]][c_2[1]] == "M":
            return True
    return False

# Part 1

def p_1():
    data = load_input()

    count = 0
    for x, line in enumerate(data):
        for y, char in enumerate(line):
            print(x, y)

            # X marks the spot, yo ho ho
            if char == 'X':
                count += word_search(x, y, data)
    
    print(count)

def word_search(x, y, data):
    next_letters = ["M", "A", "S"]
    next_coords = [(x, y)]
    
    found_count = 0
    for letter in next_letters:
        found_coords = []

        for coords in next_coords:
            if letter == "M":
                found_coords += square_search(coords[0], coords[1], letter, data)
            else:
                found_coords += directional_search(x, y, coords[0], coords[1], letter, data)
        
        if letter == "S":
            found_count = len(found_coords)
        next_coords = found_coords

    return found_count

def directional_search(x, y, n_x, n_y, match, data):
    if x > n_x:
        s_x = n_x - 1
    elif x < n_x:
        s_x = n_x + 1
    else:
        s_x = x
    
    if y > n_y:
        s_y = n_y - 1
    elif y < n_y:
        s_y = n_y + 1
    else:
        s_y = y

    if s_x >= 0 and s_y >= 0 and s_x < len(data) and s_y < len(data[0]):
        if data[s_x][s_y] == match:
            return [(s_x, s_y)]
    
    return []

def square_search(x, y, match, data):
    x_up, x, x_down = [x - 1, x, x + 1]
    y_left, y, y_right = [y - 1, y, y + 1]
    grid = [
        (x_up, y_left),
        (x_up, y),
        (x_up, y_right),
        (x, y_left),
        (x, y_right),
        (x_down, y_left),
        (x_down, y),
        (x_down, y_right)
    ]

    found = []
    for tup in grid:
        if tup[0] >= 0 and tup[1] >= 0 and tup[0] < len(data) and tup[1] < len(data[0]):
            if data[tup[0]][tup[1]] == match:
                found.append(tup)

    return found

main()