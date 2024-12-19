import random

def main():
    lines = load_input()
    avail_towels = lines[0].strip().split(', ')
    target_patterns = [x.strip() for x in lines[2:]]

    possible_count = 0
    for pattern in target_patterns:
        print(f'Testing {pattern}')

        test_count = -1
        test_limit = 1000
        pattern_index = 0
        selected_towels = []
        while True:
            test_count += 1
            if test_count == test_limit:
                print('Nope, failing this test')
                break

            # Calculate the 'score' of each towel pattern for the given pattern index
            towel_scores = {}
            for towel in avail_towels:
                score = 0
                for b, m in zip(pattern[pattern_index:], towel):
                    if b == m:
                        score += 1
                    else:
                        break
                if score > 0 and score == len(towel):
                    towel_scores[towel] = score
            
            # Check if there were no valid towel scores
            if len(towel_scores.keys()) == 0:
                print('Not possible, trying again\n')
                pattern_index = 0
                continue

            # Get the highest score
            sorted_towels = sorted(towel_scores, key=towel_scores.get, reverse=True)
            rand_int = random.randint(0, len(sorted_towels) - 1)
            top_score = sorted_towels[rand_int]

            # Increment the pattern index
            selected_towels.append(top_score)
            # print(', '.join(selected_towels))
            pattern_index += len(top_score)

            # Check our exit condition
            if pattern_index == len(pattern):
                possible_count += 1
                print('Success!\n')
                break
    
    print(f'There are {possible_count} possible combinations')

def load_input():
    with open('input.1.txt', 'r') as f:
        lines = f.readlines()
    return lines

main()