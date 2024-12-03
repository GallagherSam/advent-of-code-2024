import re

def p_2():
    lines = load_input()
    data = "".join(lines)

    total = 0
    disabled = False

    # Iterate through each character in the line
    for i, char in enumerate(data):

        # Check for next matches
        mul_match = re.search(r"mul\(\d{1,3},\d{1,3}\)", data[i:])
        do_match = re.search(r"do\(\)", data[i:])
        dont_match = re.search(r"don\'t\(\)", data[i:])

        # Check for current mul_match and not disabled state
        if mul_match and mul_match.start() == 0 and disabled == False:
            total += do_multiply(mul_match)

        # Check for current enable
        if do_match and do_match.start() == 0:
            disabled = False

        # Check for current diable
        if dont_match and dont_match.start() == 0:
            disabled = True

    print(f"Total: {total}")

def do_multiply(match):
    # Extract the numbers
    nums = re.findall(r"\d{1,3}", match.string)
    x = int(nums[0]) * int(nums[1])
    return x

def p_1():
    lines = load_input()

    total = 0
    for line in lines:
        # Find valid muls
        valid = re.findall(r"mul\(\d{1,3},\d{1,3}\)", line)

        for v in valid:
            # Extract the numbers
            nums = re.findall(r"\d{1,3}", v)
            total += int(nums[0]) * int(nums[1])

    print(total)

def load_input():
    with open("input.1.txt", "r") as f:
        lines = f.readlines()

    return lines

# IGNORE BELOW THIS... what a rabbit hole

def p_2_NOPE():
    lines = load_input()
    data = ''.join(lines)

    total = 0
    # Find valid muls
    valid = re.finditer(r"mul\(\d{1,3},\d{1,3}\)", data)

    # Find dos
    dos = re.finditer(r"do\(\)", data)
    dos = [{'start': x.start(), 'end': x.end()} for x in dos]

    # Find dont's
    donts = re.finditer(r"don\'t\(\)", data)
    donts = [{'start': x.start(), 'end': x.end()} for x in donts]

    # Find the enabled muls
    for v in valid:
        print('\nNext:\n')
        # Get closest distance for dos and donts
        do_distance = match_distance(v.start(), dos)
        dont_distance = match_distance(v.start(), donts)

        print(f'do distance: {do_distance}')
        print(f'dont distance: {dont_distance}')

        # Check start of page case
        if dont_distance < 0:
            total += do_multiply(v)
            print('Start of file')

        # Check for closer do than dont
        elif do_distance > 0 and do_distance < dont_distance:
            total += do_multiply(v)
            print('Closer do than dont')

        else:
            print('Multiply disabled')

        print('\n')
        viz(v, do_distance, dont_distance, data)
        raise Exception("PAUSE")

    print(f'Total: {total}')

def viz(v_match, do_distance, dont_distance, data):
    if do_distance < 0 and dont_distance < 0:
        end = min(do_distance, dont_distance) - 10

    do_distance = v_match.start() + abs(do_distance)
    print(do_distance)
    dont_distance = v_match.start() + abs(dont_distance)
    result = ""
    for i, char in enumerate(data[:1000]):
        if i == do_distance or i == dont_distance or i == v_match.start() or i == v_match.end() - 1:
            result += f"\033[1m{char}\033[0m"
        else:
            result += char
    
    print(result)
        
def match_distance(value, matches):
    distances = []

    for m in matches:
        distances.append(value - m['end'])

    # Check all negatives
    if all(x < 0 for x in distances) == False:
        # Mix of negatives and positives, remove negatives
        distances = [x for x in distances if x > 0]
    
    distances = sorted(distances, key=abs)

    print(distances)
    return distances[0]

p_2()