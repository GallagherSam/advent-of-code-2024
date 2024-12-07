
def main():
    lines = load_input()

    sum = 0
    for idx, line in enumerate(lines):
        print(f'Working on line {idx}')
        line = line.strip()

        # Get the test and equation
        test, equation = line.split(": ")
        test = int(test)
        equation = list(map(int, equation.split(" ")))

        # Search through the tree of operator possibilities
        equation_values = [[0]] # Numbers start at 0
        for idx, num in enumerate(equation):

            # Iter through the last values from the prior number
            last_values = equation_values[idx]
            next_values = []
            for val in last_values:
                next_values.append(val + num)
                next_values.append(val * num)
                next_values.append(int(f'{val}' + f'{num}'))
            equation_values.append(next_values)

        # Check if the test number is anywhere in the final output values
        if test in equation_values[-1]:
            print('SUCCESS!')
            sum += test
    
    print(f"Sum is: {sum}")


def load_input():
    with open('input.1.txt', 'r') as f:
        data = f.readlines()
    return data

main()