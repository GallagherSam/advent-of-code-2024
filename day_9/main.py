def main():
    data = load_input()
    
    # Create the map list
    m_list = setup_list(data)

    # Run the compact algo
    compact_p2(m_list)

    # Get the sum
    sum = 0
    for idx, i in enumerate(m_list):
        if i != '.':
            sum += idx * i
    
    print(f'Finished, sum is {sum}')

def compact_p2(m_list):
    r_list = m_list.copy()
    r_list.reverse()

    # Find groups of digits from the end of the list
    r_idx = 0
    while True:
        # If I have to do this, it means my solution runs to slowly lol
        print(r_idx, r_idx / len(r_list))

        # Check exit
        if r_idx >= len(r_list) - 1:
            break
        
        r_val = r_list[r_idx]
        # Check for real file
        if r_val != '.':
            # Calculate the start and end indexs of the group, along with the length
            start, end, length = get_group(r_idx, r_val, r_list)

            # Find the next free space that can fit
            for m_idx, m_val in enumerate(m_list):
                if m_val == '.':
                    m_start, m_end, m_length = get_group(m_idx, m_val, m_list)

                    # Check if the length is large enough
                    if m_length >= length:
                        conv_start_idx = (len(m_list) - 1) - end
                        conv_end_idx = (len(m_list) - 1) - start

                        # Validate that the found space is before the current space
                        if m_start < conv_start_idx:

                            # Add the value to this point in the list
                            for s_idx, _ in enumerate(m_list[m_start:m_start+length]):
                                m_list[m_start + s_idx] = r_val

                            # Remove the group from the end point of the list
                            for s_index in range(conv_end_idx - conv_start_idx + 1):
                                m_list[s_index + conv_start_idx] = '.'

                        break

            r_idx = end + 1

        else:
            r_idx += 1

def get_group(start_index, value, v_list):
    start = start_index
    end = 0
    length = 0
    for t_idx, t in enumerate(v_list[start_index+1:]):
        if t != value:
            end = start_index + t_idx
            break
    if end == 0:
        end = len(v_list) - 1
    length = (end - start) + 1
    return start, end, length

def compact_p1(m_list):
    r_list = m_list.copy()
    r_list.reverse()
    for r_idx, r in enumerate(r_list):

        # Check exit condition
        flag = False
        finished = True
        for i in m_list:
            if i == '.' and flag is False:
                flag = True
            elif i != '.' and flag is True:
                finished = False
        if finished:
            break

        # Find the farthest right real value
        if r != '.':
            # Iterate through the real list
            for m_idx, m in enumerate(m_list):
                # Find the next open space
                if m == '.':
                    # Update the open space to the value
                    m_list[m_idx] = r
                    # Update the prior space to be open
                    m_list[(len(m_list) - 1) - r_idx] = '.'
                    break

def setup_list(data):
    m_list = []
    id = 0
    free_space_toggle = False
    for char in data:
        size = int(char)
        val = '.'

        # Check for free vs. non free space
        if free_space_toggle is False: # REAL DATA
            free_space_toggle = not free_space_toggle
            val = id
            id += 1
        else: # FREE SPACE
            free_space_toggle = not free_space_toggle

        for _ in range(size):
            m_list.append(val)
    return m_list

def visualize(m_list):
    print(''.join([f'{x}' for x in m_list]))

def load_input():
    with open('input.1.txt', 'r') as f:
        lines = f.readlines()
    return lines[0]


main()