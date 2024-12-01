def sim_score():
    # Load input
    left_list, right_list = load_input()

    # Calculate similarity
    sim_cache = {}
    sims = []
    for left in left_list:
        # Check the cache
        if left in sim_cache:
            sims.append(sim_cache[left])
            continue

        # Calculate new number
        count = 0
        for right in right_list:
            if right == left:
                count += 1

        # Calculate similarity
        sim_score = left * count

        # Update sim cache and sim score
        sim_cache[left] = sim_score
        sims.append(sim_score)

    # Sum the similarities
    sim_sum = sum(sims)
    print(sim_sum)


def distance_sum():
    # Load input
    left_list, right_list = load_input()

    # Sort the lists
    left_list = sorted(left_list)
    right_list = sorted(right_list)

    # Calculate distances
    distances = []
    for idx, left in enumerate(left_list):
        right = right_list[idx]
        distances.append(abs(right - left))

    # Sum the distances
    distance_sum = sum(distances)
    print(distance_sum)


def load_input():
    # Load the list
    with open("input.1.txt", "r") as f:
        lines = f.readlines()

    # Extract the lists
    left_list = []
    right_list = []
    for line in lines:
        left, right = map(int, line.split())
        left_list.append(left)
        right_list.append(right)

    return left_list, right_list


sim_score()
