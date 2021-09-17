from itertools import combinations
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


def convert_dict_to_price_list(dataset):
    price_list2 = []
    for key in dataset:
        price_list2.append((key, dataset[key][0]))
    return price_list2


def sorted_price_list(price_list2):
    price_list2.sort(key=lambda action1: action1[1])
    return price_list2


def calculate_max_size_wallet_length(price_list_ordered):
    max_size_wallet = []
    total_cost2 = 0
    for action in price_list_ordered:
        total_cost2 += action[1]
        max_size_wallet.append(action)
        if total_cost2 > 500:
            total_cost2 -= action[1]
            max_size_wallet.pop()
    return len(max_size_wallet)


def calculate_min_size_wallet_length(price_list_ordered):
    price_list_ordered.reverse()
    max_size_wallet = []
    total_cost2 = 0
    for action in price_list_ordered:
        total_cost2 += action[1]

        if total_cost2 > 500:
            total_cost2 -= action[1]
        else:
            max_size_wallet.append(action)
    price_list_ordered.reverse()
    return len(max_size_wallet)


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

sorted_list = sorted_price_list(convert_dict_to_price_list(base_dataset))
max_list = calculate_max_size_wallet_length(sorted_list)
min_list = calculate_min_size_wallet_length(sorted_list)

all_combinations = []
final_combinations = []
start_all = time.perf_counter()
for i in range(max_list, (min_list - 1), -1):
    start_number = time.perf_counter()
    all_possible_combinations = combinations(base_dataset, i)
    all_possible_combinations_with_ROI = []
    for combination in all_possible_combinations:
        total_ROI = 0.0
        total_cost = 0.0
        final_combination = []
        # Calculate global ROI of wallet
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

    print(f"résultats {i} :")
    print("sans doublons:")
    print(len(all_combinations))

    print(i)
    print("duration:")
    print(elapsed_time_formatted(start_number))
    print()
    print("duration from beginning:")
    print(elapsed_time_formatted(start_all))
    print()

print("LAST RESULTS")
print(len(all_combinations))

all_combinations.sort(key=lambda combi: combi[2], reverse=True)

for i in range(0, 10):
    print("10 meilleurs :")
    print(all_combinations[i])

print()

for i in range(10, 0, -1):
    print("10 pires :")
    print(all_combinations[-i])

print("longueur du meilleur: ")
print(len(all_combinations[0][0]))
print("Le grand gagnant est:")
print(all_combinations[0])
print()
print("total_duration:")
print(elapsed_time_formatted(start_all))
