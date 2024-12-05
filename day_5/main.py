sanity_order_length = []
incorrect_mid_sum = 0

def p_2():
    global incorrect_mid_sum, sanity_order_length
    data = load_input()

    for idx, order in enumerate(data['orders']):
        print(f"Order: {idx}")
        pages = order.split(',')

        if check_rules(pages, data['rules']) is False:
            # Rule was broken, lets fix it
            fix_order(pages, data['rules'])

    print(f'Part 2 Sum: {incorrect_mid_sum}')

def p_1():
    global incorrect_mid_sum, sanity_order_length
    data = load_input()

    middle_sum = 0
    for idx, order in enumerate(data['orders']):
        print(f"Order: {idx}")
        pages = order.split(',')

        if check_rules(pages, data['rules']):
            sanity_order_length.append(pages)
            middle_sum += get_middle_value(pages)
        

    print(f'Part 1 Sum: {middle_sum}')


def check_rules(pages, rules):
    flag = True
    # Iterate through the following pages
    for idx, x_p in enumerate(pages):
        for y_p in pages[idx+1:]:

            # Iterate through the rules
            for rule in rules:
                left, right = rule.split('|')

                # Check if the left equals the following page from current, and right equal the current page
                if left == y_p and right == x_p:
                    # This means a rule is broken, as a following page to current has a rule to be in front
                    flag = False
                    break
            
            # We don't need to check anymore pages as a rule is broken
            if flag == False:
                break
    
    return flag

def fix_order(pages, rules):
    global incorrect_mid_sum, sanity_order_length
    new_order = pages.copy()

    # Iterate through the pages
    for idx, x_p in enumerate(pages):
        for y_p in pages[idx+1:]:

            # Iterate through the rules
            for rule in rules:
                left, right = rule.split('|')
                if left == y_p and right == x_p:
                    # Identified a broken rule, move y_p in front of x_p
                    new_order.remove(y_p)
                    new_idx = new_order.index(x_p)
                    new_order.insert(new_idx, y_p)

    # Sanity check the rules
    if check_rules(new_order, rules) is False:
        fix_order(new_order, rules)
    
    else:
        mid = get_middle_value(new_order)
        incorrect_mid_sum += mid
        sanity_order_length.append(new_order)

def get_middle_value(pages):
    mid = int((len(pages) - 1) / 2)
    return int(pages[mid])

def load_input():
    with open('input.1.txt', 'r') as f:
        lines = f.readlines()

    data = {
        'rules': [],
        'orders': []
    }
    flag = False
    for line in lines:
        if line == '\n':
            flag = True
            continue
        if flag is False:
            data['rules'].append(line.strip())
        else:
            data['orders'].append(line.strip())
    
    return data

p_2()