import re

# Globals
GRID_X = 101 # 11
GRID_X_HALF = 50
GRID_Y = 103 #7
GRID_Y_HALF = 51

class Robot:
    def __init__ (self, line):
        pattern = r'p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)'
        matches = re.match(pattern, line)
        self.p_x, self.p_y, self.v_x, self.v_y = map(int, matches.groups())

    def update(self, debug=False):
        if debug:
            print(f'Starting coords ({self.p_x}, {self.p_y})')

        # Straight update from velocity
        self.p_x += self.v_x
        self.p_y += self.v_y

        # Check if we need to wrap around
        if self.p_x < 0:
            self.p_x += GRID_X
        elif self.p_x >= GRID_X:
            self.p_x -= GRID_X
        
        if self.p_y < 0:
            self.p_y += GRID_Y
        elif self.p_y >= GRID_Y:
            self.p_y -= GRID_Y

        if debug:
            print(f'Ending coords ({self.p_x}, {self.p_y})')

    def __repr__(self):
        return f'<ROBOT {self.p_x}, {self.p_y} -> {self.v_x}, {self.v_y}>'

def main():
    lines = load_input()

    # Create a list of Robot objects
    robots = generate_robots(lines)

    # Tick forward x times
    tick_times = 10000
    for i in range(tick_times):
        print(i+1)
        # print(f'{round(i+1 / tick_times, 4)}%') 12 - h, 35 - v, 115 - h, 136 - v

        # Stop to display the robots during the h and v patters
        if check_if_pattern_frame(i):
            visualize_robots(robots)
            input()

        # Update each robot position
        for robot in robots:
            robot.update()
        
        # visualize_robots(robots)
        # input()
    
    # Take a look at the robots final configuration
    visualize_robots(robots)

    p1_ans = count_robot_quarters(robots)
    print(f'p1 {p1_ans}')

def check_if_pattern_frame(i):
    x = i + 0
    flag = False
    if x == 12 or x == 35:
        flag = True

    # Check h
    h = x + 0
    while True:
        if h > GRID_Y:
            h -= GRID_Y
        else:
            break
        
        if h - 12 == 0:
            flag = True
            break
    
    # Check v
    while True:
        if x > GRID_X:
            x -= GRID_X
        else:
            break

        if x - 35 == 0:
            flag = True
            break
    
    return flag


def count_robot_quarters(robots):
    q1, q2, q3, q4 = 0, 0, 0, 0

    # Distribute the robot coords properly
    robot_coords = {}
    for robot in robots:
        key = f'{robot.p_x}, {robot.p_y}'
        if key in robot_coords:
            robot_coords[key] += 1
        else:
            robot_coords[key] = 1

    for y in range(GRID_Y):
        for x in range(GRID_X):
            key = f'{x}, {y}'

            if key in robot_coords:
                if y < GRID_Y_HALF and x < GRID_X_HALF: #q1
                    q1 += robot_coords[key]
                elif y < GRID_Y_HALF and x > GRID_X_HALF: #q3
                    q3 += robot_coords[key]
                elif y > GRID_Y_HALF and x < GRID_X_HALF: #q2
                    q2 += robot_coords[key]
                elif y > GRID_Y_HALF and x > GRID_X_HALF: #q4
                    q4 += robot_coords[key]
    
    print(q1, q2, q3, q4)
    return q1 * q2 * q3 * q4

def visualize_robots(robots):
    robot_coords = {}
    for robot in robots:
        key = f'{robot.p_x}, {robot.p_y}'
        if key in robot_coords:
            robot_coords[key] += 1
        else:
            robot_coords[key] = 1
    
    for x in range(GRID_Y):
        out_str = ""
        for y in range(GRID_X):
            key = f'{y}, {x}'
            if key in robot_coords:
                out_str += f'{robot_coords[key]}'
            else:
                out_str += '.'
        print(out_str)

def generate_robots(lines):
    robots = []
    for line in lines:
        line = line.strip()
        robots.append(Robot(line))
    return robots

def load_input():
    with open('input.1.txt', 'r') as f:
        lines = f.readlines()
    return lines

main()