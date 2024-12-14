import math

A_COST = 1
B_COST = 3

def main():
    data = load_input()

    # Break apart the input
    button_a = False
    button_b = False
    prize = False
    p1 = 0
    for line in data:
        line = line.strip()

        # Parse the lines
        if 'Button A' in line:
            x = int(line.split('X+')[1].split(', ')[0])
            y = int(line.split('Y+')[1])
            button_a = {'x': x, 'y': y}
        elif 'Button B' in line:
            x = int(line.split('X+')[1].split(', ')[0])
            y = int(line.split('Y+')[1])
            button_b = {'x': x, 'y': y}
        elif 'Prize' in line:
            x = int(line.split('X=')[1].split(', ')[0])
            y = int(line.split('Y=')[1])
            prize = {'x': x, 'y': y}

        # Check for valid combination
        if button_a and button_b and prize:
            print(button_a, button_b, prize)
            
            # Do the math stuff
            if check_if_solvable(button_a, button_b, prize):
                ret = solve(button_a, button_b, prize)
                print(ret)
                p1 += ret[2]

            else:
                print('This one is unsolvable')

            # Revert values
            button_a = False
            button_b = False
            prize = False

    print(f'p1: {p1}')

# I'm definitely gonna need some notes to keep the math straight
# We want to find a valid (m_x, n_x) count of transformations to plug in, giving us a starting point
# m*button_a[x] + n*button_b[x] = prize[x]
def solve(button_a, button_b, prize):
    # Get the extended gcd for the x axis
    g = abs(extended_gcd(button_a['x'], button_b['x'])[0])

    # Scale down to that gcd
    button_a_xp, button_b_xp, prize_xp = button_a['x']//g, button_b['x']//g, prize['x']//g

    # Roll up math sleeves, do extended euclidean algorithm
    g2, u, v = extended_gcd(button_a_xp, button_b_xp)
    if g2 != 1:
        raise Exception(f"The math didn't math properly, g2 is {g2}")

    # Scale the solution back up
    m_x = u * prize_xp
    n_x = v * prize_xp

    # Use a k coefficient to find Y and the lowest cost
    a, b = button_a_xp, button_b_xp
    K_coeff = button_a['y']*b - button_b['y']*a
    const_term = prize['y'] - (button_a['y']*m_x + button_b['y']*n_x)

    if K_coeff == 0:
        # Then either we already satisfy Y or it's impossible.
        if const_term == 0:
            k_candidates = []
            for k_test in range(-1000, 1001):
                m_test = m_x + b*k_test
                n_test = n_x - a*k_test
                if m_test >= 0 and n_test >= 0:
                    k_candidates.append((m_test, n_test, m_test*A_COST + n_test*B_COST))
            if not k_candidates:
                return None
            # Return the minimal cost solution
            return min(k_candidates, key=lambda x: x[2])
        else:
            return None
    else:
        # K_equation: K_coeff * k = const_term
        if const_term % K_coeff != 0:
            return None  # No integer k if remainder != 0
        k = const_term // K_coeff

        # Compute m,n for this k
        m_final = m_x + b*k
        n_final = n_x - a*k

        if m_final < 0 or n_final < 0:

            k_candidates = []
            for k_test in range(k-2000, k+2001):
                m_test = m_x + b*k_test
                n_test = n_x - a*k_test
                if m_test >= 0 and n_test >= 0:
                    k_candidates.append((m_test, n_test, m_test*A_COST + n_test*B_COST))
            if not k_candidates:
                return None
            return min(k_candidates, key=lambda x: x[2])
        else:
            return (m_final, n_final, m_final*A_COST + n_final*B_COST)

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)


def check_if_solvable(button_a, button_b, prize):
    flag = True
    for n in ['x', 'y']:
        gcd = math.gcd(button_a[n], button_b[n])
        if prize[n] % gcd != 0:
            flag = False
    return flag

def load_input():
    with open('input.2.txt', 'r') as f:
        data = f.readlines()
    return data

main()