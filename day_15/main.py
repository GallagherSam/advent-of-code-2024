
class Game:
    def __init__(self, objects, input_commands):
        self.objects = objects
        self.robot = [obj for obj in objects if isinstance(obj, Robot)][0]
        self.input_commands = input_commands

    def run(self, debug=False):
        if debug:
            print('Initial State:')
            self.visualize()

        for command in self.input_commands:
            # Get the coordinates from the robot if it were to attempt moving this way
            dry_top, dry_right = self.robot.attempt_move(command)

            if debug:
                print(f'Robot will try moving to ({dry_top}, {dry_right}) from ({self.robot.top}, {self.robot.right}) as the direction is ({command})')

            # See if there is an object there
            obj = self.get_coords(dry_top, dry_right)
            if obj: # Yup something in the way, let's deal with it
                
                if debug:
                    print(f'There is an object in the way {obj}.')

                if isinstance(obj, Wall): # It's a wall! Can't move

                    if debug:
                        print(f'Its a wall, cant move.')

                elif isinstance(obj, Box): # It's a box, we have to see if it can be pushed

                    if debug:
                        print(f'Its a box, check if it can be shoved')

                    # Keep looking in the direction of movement until we either see open space or a wall, tracking the boxes we find along the way
                    boxes = [obj]
                    search_top, search_right = dry_top + 0, dry_right + 0
                    while True:

                        # Get the next coord
                        if command == 'up':
                            search_top -= 1
                        elif command == 'right':
                            search_right += 1
                        elif command == 'down':
                            search_top += 1
                        elif command == 'left':
                            search_right -= 1


                        # Check what's at that coord
                        search_obj = self.get_coords(search_top, search_right)
                        if debug:
                            print(f'Box shove searching at ({search_top}, {search_right}) and found {search_obj}')

                        if isinstance(search_obj, Box): # Add boxes to the pile
                            boxes.append(search_obj)
                        elif isinstance(search_obj, Wall): # We cancel the search at a wall
                            break
                        else: # There is empty space, we can move the robot and shove the boxes forward
                            
                            # Move the boxes
                            boxes = list(set(boxes))

                            if debug:
                                print('Here are the found boxes')
                                print(boxes)

                            for box in boxes:
                                box.move(command)
                            
                            # Move the robot
                            self.robot.move(command)
                            break

                elif isinstance(obj, BigBox): # It's a big box, shoving is more complicated

                    if debug:
                        print(f'Its a BigBox, checking what we need to shove')

                    # Keep track of the boxes that need to be shoved
                    boxes = [obj]
                    
                    # Recursively check the boxes to see if there are more that need to be shoved
                    while True:
                        
                        exit_flag = False
                        move_flag = True

                        for box in boxes:
                            search_top, search_right = dry_top + 0, dry_right + 0

                            search_coords = []
                            # Get the next coord
                            if command == 'up':
                                search_top -= 1
                                search_coords.append((search_top, box.right), (search_top, box.width))
                            elif command == 'right':
                                search_right += 1
                            elif command == 'down':
                                search_top += 1
                                search_coords.append((search_top, box.right), (search_top, box.width))
                            elif command == 'left':
                                search_right -= 1
                            search_coords.append((search_top, search_right))

                            if debug:
                                print(f'Here are the BigBox search coords {search_coords}')

                            for coord in search_coords:
                                search_obj = self.get_coords(coord[0], coord[1])

                                # Skip self
                                if box == search_obj:
                                    continue

                                if debug:
                                    print(f'BigBox search for {box} found {search_obj} at ({coord})')

                                if isinstance(search_obj, BigBox): # We found a box, add it to the pile
                                    boxes.append(search_obj)
                                    move_flag = False
                                elif isinstance(search_obj, Wall): # We found a wall, stop the search
                                    exit_flag = True
                                    break
                        
                        if exit_flag:
                            break

                        if move_flag: # We can move things
                            boxes = list(set(boxes))

                            for box in boxes:
                                box.move(command)
                            
                            self.robot.move(command)
                            break


            else: # Nope, robot can freely move
                
                if debug:
                    print(f'Robot is moving to ({dry_top}, {dry_right}) as there is nothing in the way.')

                self.robot.move(command)
        
            if debug:
                self.visualize()
                input()

    def visualize(self):
        max_bottom, max_right = self._max_bottom(), self._max_right()

        for top in range(max_bottom):
            out_str = ""
            for right in range(max_right):
                obj = self.get_coords(top, right, for_visual=True)
                if obj != None and obj != False:
                    out_str += obj.char
                elif obj == None:
                    out_str += '.'
                else:
                    continue
            print(out_str)

    def get_coords(self, top, right, for_visual=False):
        out = None
        for obj in self.objects:
            if obj.top == top and obj.right == right:
                out = obj
                break
            elif isinstance(obj, BigBox) and obj.top == top and obj.width == right:
                if for_visual:
                    out = False
                else:
                    out = obj
                break
        return out

    def sum_p1(self):
        out = 0
        for obj in self.objects:
            if isinstance(obj, Box) or isinstance(obj, BigBox):
                x = 100 * obj.top
                out += x + obj.right
        return out

    def _max_bottom(self):
        out = 0
        for obj in self.objects:
            if obj.top > out:
                out = obj.top
        return out + 1
    
    def _max_right(self):
        out = 0
        for obj in self.objects:
            if isinstance(obj, BigBox):
                test = obj.width
            else:
                test = obj.right

            if test > out:
                out = obj.right
        return out + 1

class GameObject:
    def __init__(self, top, right):
        self.top = top
        self.right = right

    def move(self, direction):
        top, right = self._get_dir_coord(direction)
        self.top = top
        self.right = right

    def _get_dir_coord(self, direction):
        dry_top, dry_right = self.top + 0, self.right + 0

        if direction == 'up':
            dry_top -= 1
        elif direction == 'right':
            dry_right += 1
        elif direction == 'down':
            dry_top += 1
        elif direction == 'left':
            dry_right -= 1
        else:
            raise Exception(f'{direction} is not a valid direction to move.')
        
        return (dry_top, dry_right)
    
    def __repr__(self):
        return f'<{self.name} - ({self.top}, {self.right})>'


class Robot(GameObject):
    def __init__(self, top, right):
        super().__init__(top, right)
        self.char = '@'
        self.name = 'Robot'

    def attempt_move(self, direction):
        return self._get_dir_coord(direction)

class Wall(GameObject):
    def __init__(self, top, right):
        super().__init__(top, right)
        self.char = '#'
        self.name = 'Wall'

class Box(GameObject):
    def __init__(self, top, right):
        super().__init__(top, right)
        self.char = '0'
        self.name = 'Box'

class BigBox(GameObject):
    def __init__(self, top, right):
        super().__init__(top, right)
        self.width = right + 1
        self.char = '[]'
        self.name = 'BigBox'
    
    def move(self, direction):
        dry_top, dry_right = self._get_dir_coord(direction)
        self.top = dry_top
        self.right = dry_right
        self.width = self.right + 1

def p2():
    lines = load_input()
    object_lines = stretch_input(lines)
    objects = generate_objects(object_lines)
    input_commands = parse_input_commands(lines)
    game = Game(objects, input_commands)
    game.run(debug=True)
    game.visualize()
    p2_solution = game.sum_p1()

    print(f'P2 ans: {p2_solution}')

def p1():
    lines = load_input()
    objects = generate_objects(lines)
    input_commands = parse_input_commands(lines)
    game = Game(objects, input_commands)
    game.run()
    game.visualize()
    p1_solution = game.sum_p1()

    print(f'P1 ans: {p1_solution}')

def stretch_input(lines):
    out = []
    for line in lines:
        line = line.strip()
        if line == '' or line[0] != '#':
            break
        out_str = ''
        for char in line:
            if char == '#':
                out_str += '##'
            elif char == 'O':
                out_str += '[]'
            elif char == '@':
                out_str += '@.'
            else:
                out_str += '..'
        out.append(out_str)
    return out

def generate_objects(lines):
    objects = []
    for top, line in enumerate(lines):
        line = line.strip()
        if line == '': # Stop at the blank
            break
    
        for right, char in enumerate(line):
            if char == '#':
                objects.append(Wall(top, right))
            elif char == 'O':
                objects.append(Box(top, right))
            elif char == '@':
                objects.append(Robot(top, right))
            elif char == '[':
                objects.append(BigBox(top, right))
            elif char == ']':
                continue

    return objects

def parse_input_commands(lines):
    out = []
    for line in lines:
        line = line.strip()
        if line == '' or line[0] == '#':
            continue
        for char in line:
            if char == '^':
                out.append('up')
            elif char == '>':
                out.append('right')
            elif char == 'v':
                out.append('down')
            elif char == '<':
                out.append('left')
    return out

def load_input():
    with open('input.2.txt', 'r') as f:
        lines = f.readlines()
    return lines

p2()