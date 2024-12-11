import time

def p_2(): # Maybe overly optimistic
    data = load_input()

    # Split into numbers
    nums = list(map(int, data.split(' ')))

    # Create the distribution map
    nums_map = {}
    for num in nums:
        if num not in nums_map:
            nums_map[num] = 1
        else:
            nums_map[num] += 1

    # Iterate through the blinks
    blink_count = 75
    for i in range(blink_count):
        # print(nums_map)
        start_time = time.time()
        new_map = {}

        for key in nums_map.keys():
            # print('key', key)
            num_count = nums_map[key]
            blink_vals = blink(key)
            # print('blink_vals', blink_vals)
            for val in blink_vals:
                if val in new_map:
                    new_map[val] += num_count
                else:
                    new_map[val] = num_count
                # print(new_map)
        nums_map = new_map

        end_time = time.time()
        dur = round(end_time - start_time, 4)
        # print(f'Duration: {dur}')
        # input()

    print(f'Q2: {calc_length_from_map(nums_map)}')
            

def calc_length_from_map(nums_map):
    sum = 0
    for key in nums_map.keys():
        sum += nums_map[key]
    return sum

def p_1():
    data = load_input()

    # Split into numbers
    nums = list(map(int, data.split(' ')))

    # Run the blink phenom
    blink_count = 25
    for i in range(blink_count):
        print(i+1, len(nums))
        next_nums = []
        for num in nums:
            new_nums = blink(num)
            next_nums += new_nums
        nums = next_nums
    
    # Count the numbers
    count = len(nums)
    print(f'There are {count} stones')

def blink(num):
    out = []

    if num == 0: # In comes 0, out comes 1
        out.append(1)
    
    elif len(f'{num}') % 2 == 0: # Split it up 🔪
        str = f'{num}'
        str_mid = len(str) // 2
        left, right = int(str[:str_mid]), int(str[str_mid:])
        out.append(left)
        out.append(right)
    
    else:
        out.append(num * 2024)
    
    return out

def load_input():
    with open('input.1.txt', 'r') as f:
        data = f.readlines()
    return data[0].strip()

if __name__ == '__main__':
    p_2()