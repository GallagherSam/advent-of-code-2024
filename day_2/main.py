def safe_assessment():
    # Load the input
    lines = load_input()

    # Split into lines of ints
    levels = []
    for line in lines:
        x = map(int, line.split())
        y = []
        for x in x:
            y.append(x)
        levels.append(y)

    safe_reports = problem_dampener_wrapper(levels)
    print(safe_reports)


def problem_dampener_wrapper(levels):
    safe_count = 0

    # Check all permuations of the levels
    for x in levels:

        # Do the initial one
        is_safe = check_safe_report(x)
        if is_safe:
            safe_count += 1
            continue

        # Check all combinations
        for idx, _ in enumerate(x):
            c = x.copy()
            c.pop(idx)
            is_safe = check_safe_report(c)
            if is_safe:
                safe_count += 1
                break

    return safe_count


def check_safe_report(l):
    # Check for asc or dsc
    asc_flag = False
    dsc_flag = False
    unsafe = False
    for idx, x in enumerate(l):
        if idx == 0:
            continue

        if x > l[idx-1] and dsc_flag == True:
            unsafe = True
            break

        elif x > l[idx-1] and asc_flag == False:
            asc_flag = True

        elif x < l[idx-1] and asc_flag == True:
            unsafe = True
            break

        elif x < l[idx-1] and dsc_flag == False:
            dsc_flag = True

    if unsafe:
        return False

    # Check for adjacency rules, differ by at least 1 but not more than 3
    for idx, x in enumerate(l):
        if idx == 0:
            continue

        diff = abs(x - l[idx-1])
        if diff == 0 or diff > 3:
            unsafe = True
            break

    if unsafe:
        return False

    return True


def load_input():
    with open('input.1.txt', 'r') as f:
        lines = f.readlines()
    return lines


safe_assessment()
