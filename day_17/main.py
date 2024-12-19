
def main():
    lines = [x.strip() for x in load_input()]

    reg_a, reg_b, reg_c = load_registers(lines)
    program_codes = load_program_codes(lines)
    print(reg_a, reg_b, reg_c, program_codes)

def load_program_codes(lines):
    out = []

    for line in lines:
        if 'Program:' in line:
            codes = line.split(': ')[1]
            out = list(map(int, codes.split(',')))
            break
    
    return out

def load_registers(lines):
    reg_a, reg_b, reg_c = 0, 0, 0

    for line in lines:
        if 'Register A' in line:
            reg_a = int(line.split(': ')[1])
        elif 'Register B' in line:
            reg_b = int(line.split(': ')[1])
        elif 'Register C' in line:
            reg_c = int(line.split(': ')[1])
        else:
            break

    return reg_a, reg_b, reg_c

def load_input():
    with open('input.2.txt', 'r') as f:
        lines = f.readlines()
    return lines

main()