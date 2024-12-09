
def main():
    # Load the file
    data = load_input()

    # Create the starting state map
    c_map = create_starting_map(data)
    visualize(c_map)

    # Run the compaction algorithm
    compaction(c_map)

    # Sum for final output
    sum = sum_map(c_map)
    
    visualize(c_map)
    print(f'P1 sum {sum}')

def sum_map(c_map):
    sum = 0

    # Loop through the map and multiple the new index by the id
    idx = 0
    for m in c_map:
        if m['id'] != 'free':
            # For real files, iterate through the range to multiply
            for i in range(idx, idx + m['length']):
                sum += i * m['id']
            idx += m['length']

    return sum
    
def compaction(c_map):
    while True:
        # input()
        # Join consecutive groups (by id) of file blocks together, join empties
        garbage_collect(c_map)

        # Check exit condition (solid block of numbers then solid block of empties)
        if check_finished(c_map):
            break

        # Find the next last block in the series
        next_block = get_last_block(c_map)

        # For it's length, find a spot to compact it to, updating the map
        for i in range(next_block['length']):
            compact_digit(next_block, c_map)

def garbage_collect(c_map):
    while True:
        flag = False
        # Check if we have duplicates
        for m in c_map:
            matches = [x for x in c_map if x['id'] == m['id']]
            if len(matches) > 1:
                flag = True
                break
        if flag:
            success = garbage_collect_exec(c_map)
            if success is False:
                break
        else:
            break

def garbage_collect_exec(c_map):
    # Find next door blocks by id and combine them
    flag = False
    idx = 0
    while True:
        if (idx + 1) < len(c_map):
            m = c_map[idx]
            n = c_map[idx + 1]
            if m['id'] == n['id']:
                m['length'] += n['length']
                c_map.remove(n)
                flag = True
            idx += 1
        else:
            break
    return flag

def check_finished(c_map):
    # We know it's finished if there are no free blocks mingled with file blocks
    finished = True
    found_empty = False
    for m in c_map:
        if m['id'] == 'free' and found_empty is False:
            found_empty = True
        
        if m['id'] != 'free' and found_empty is True:
            finished = False
            break
    return finished

def get_last_block(c_map):
    block = None
    for m in c_map:
        if m['id'] != 'free':
            block = m
    return block

def compact_digit(next_map, c_map):
    print('compact')
    visualize(c_map)
    input()
    for idx, m in enumerate(c_map):

        # Find the next free space
        if m['id'] == 'free':

            # Insert the digit in front of the free space
            c_map.insert(c_map.index(m), {
                'id': next_map['id'],
                'length': 1
            })

            # Add free space where this digit moved from
            free_index = c_map.index(next_map) + 1
            if free_index >= len(c_map):
                c_map.append({
                    'id': 'free',
                    'length': 1
                })
            else:
                c_map.insert(free_index, {
                    'id': 'free',
                    'length': 1
                })

            # Reduce the length of the next map
            next_map['length'] -= 1
            if next_map['length'] <= 0:
                c_map.remove(next_map)

            # Reduce the length of the free space
            if m['length'] > 1:
                m['length'] -= 1
            else:
                c_map.pop(idx)
            
            break


def create_starting_map(data):
    starting_map = []

    # Iterate through the characters
    free_space_flag = False
    id = 0
    for char in data:
    
        if free_space_flag is False: # Real data
            item = {
                'id': id,
                'length': int(char)
            }
            free_space_flag = not free_space_flag
            id += 1
        else:
            item = {
                'id': 'free',
                'length': int(char)
            }
            free_space_flag = not free_space_flag

        starting_map.append(item)

    return starting_map

def visualize(c_map):
    string = ""
    for m in c_map:
        for _ in range(m['length']):
            if m['id'] != 'free':
                string += f"{m['id']}"
            else:
                string += '.'
    print(string)

def load_input():
    with open('input.2.txt', 'r') as f:
        lines = f.readlines()
    return lines[0]


main()