from itertools import combinations, combinations_with_replacement, permutations
import time


def factorielle(n):
    if n == 0:
        return 1
    else:
        f = 1
        for k in range(2, n+1):
            f = f * k
        return f


def possibility_calculation(total_number, wallet_size):
    return factorielle(total_number) / factorielle(total_number-wallet_size) / factorielle(wallet_size)


def elapsed_time_formatted(begin_time):
    """
    Calculates difference between begin_time and actual time,
    and formats it in HH:MM:SS.
    :param begin_time: time we want to compare with, in seconds.
    """
    return time.strftime(
        "%H:%M:%S", (time.gmtime(time.perf_counter() - begin_time))
    )


base_dataset = {
    "Action-1": (20, 5),
    "Action-2": (30, 10),
    "Action-3": (50, 15),
    "Action-4": (70, 20),
    "Action-5": (60, 17),
    "Action-6": (80, 25),
    "Action-7": (22, 7),
    "Action-8": (26, 11),
    "Action-9": (48, 13),
    "Action-10": (34, 27),
    "Action-11": (42, 17),
    "Action-12": (110, 9),
    "Action-13": (38, 23),
    "Action-14": (14, 1),
    "Action-15": (18, 3),
    "Action-16": (8, 8),
    "Action-17": (4, 12),
    "Action-18": (10, 14),
    "Action-19": (24, 21),
    "Action-20": (114, 18)
}

# all_possible_16_combinations = combinations(base_dataset, 20)

# print(all_possible_16_combinations)
all_combinations = []
final_combinations = []
start_all = time.perf_counter()
for i in range(20, 1, -1):
    start_number = time.perf_counter()
    j = i
    print(i)
    print(i)
    print(i)
    all_possible_combinations = combinations(base_dataset, i)
    all_possible_combinations_with_ROI = []
    for combination in all_possible_combinations:
        # print(combination)
        total_ROI = 0.0
        total_cost = 0.0
        final_combination = []
        # Calculate global ROI
        for element in combination:
            total_cost += base_dataset[element][0]
            if total_cost > 500:
                total_cost -= base_dataset[element][0]
                break
            total_ROI += base_dataset[element][0]*base_dataset[element][1]/100
            final_combination.append(element)

        final_combination_with_ROI = (final_combination, total_cost, total_ROI)
        if final_combination_with_ROI not in all_combinations:
            all_combinations.append(final_combination_with_ROI)

    print(f"resultats {i}")
    print("sans doublons:")
    print(len(all_combinations))

    # all_possible_16_combinations_with_ROI = list(set(all_possible_16_combinations_with_ROI))

    # all_possible_16_combinations_with_ROI.sort(key=lambda combi: combi[2], reverse=True)

    # if len(all_possible_16_combinations_with_ROI) > 10:
    #     for j in range(0, 10):
    #         print(all_possible_16_combinations_with_ROI[j])
    #     print()
    #     for j in range(10, 0, -1):
    #         print(all_possible_16_combinations_with_ROI[-j])
    # else:
    #     for combination in all_possible_16_combinations_with_ROI:
    #         print(combination)
    # print()
    # print("longueur du meilleur:")
    # print(len(all_possible_16_combinations_with_ROI[0][0]))
    # all_combinations.extend(all_possible_16_combinations_with_ROI)
    print()
    print("last one i")
    print(i)
    print("duration:")
    print(elapsed_time_formatted(start_number))
    print()
    print("duration from beginning:")
    print(elapsed_time_formatted(start_all))
    print()

# for combination in all_combinations:
#     if combination not in final_combinations:
#         final_combinations.append(combination)

print("LAST RESULTS")
print(len(final_combinations))

final_combinations.sort(key=lambda combi: combi[2], reverse=True)

for i in range(0, 10):
    print("10 meilleurs :")
    print(final_combinations[i])

print()

for i in range(10, 0, -1):
    print("10 pires :")
    print(final_combinations[-i])

print("longueur du meilleur: ")
print(len(final_combinations[0][0]))
print("Le grand gagnant est:")
print(final_combinations[0])
print()
print("total_duration:")
print(elapsed_time_formatted(start_all))
