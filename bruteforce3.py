from itertools import combinations
import time

import tablib


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
        if total_cost2 > 500:
            total_cost2 -= action[1]
        else:
            max_size_wallet.append(action)
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


def create_database(dict_data):
    dataset = tablib.Dataset()
    dataset.headers = ['name', 'price', 'profit']
    for entry, value in dict_data.items():
        dataset.append([entry, value[0], value[1]])
    print(dataset.export('csv'))
    with open('dataset.csv', 'w') as file:
        file.write(dataset.export('csv'))


def open_convert_and_clean_csv(csv_data_file):
    imported_data = tablib.Dataset().load(open(csv_data_file).read())
    dataset = []
    for row in imported_data:
        if float(row[1]) > 0 and float(row[2]) > 0:
            dataset.append((row[0], float(row[1]), float(row[2])))
    return dataset


base_dataset = open_convert_and_clean_csv('dataset_training.csv')

print(f"dataset size = {len(base_dataset)}")

start_all = time.perf_counter()
sorted_list = sorted_price_list(base_dataset)
print("list sorted")
print("duration from beginning:")
print(elapsed_time_formatted(start_all))
max_list_size = calculate_max_size_wallet_length(sorted_list)
print(f"max found : {max_list_size}")
print("duration from beginning:")
print(elapsed_time_formatted(start_all))
min_list_size = calculate_min_size_wallet_length(sorted_list)
print(f"min found : {min_list_size}")
print("duration from beginning:")
print(elapsed_time_formatted(start_all))

all_combinations = []
for i in range(min_list_size, (max_list_size + 1)):
    start_number = time.perf_counter()
    print()
    print(f"beginning of {i} :")
    print("duration:")
    print(elapsed_time_formatted(start_number))
    print()
    print("duration from beginning:")
    print(elapsed_time_formatted(start_all))
    print()
    all_possible_combinations = combinations(base_dataset, i)
    final_combinations = []
    for combination in all_possible_combinations:
        final_combination = []
        total_ROI = 0.0
        total_cost = 0.0
        # Calculate global ROI of wallet
        for element in combination:
            total_cost += element[1]
            total_ROI += (element[1]*element[2])/100
            final_combination.append(element)

        if total_cost <= 500:
            final_combination_with_ROI = (final_combination, total_cost, total_ROI)
            all_combinations.append(final_combination_with_ROI)

    print(f"résultats {i} :")
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

print("10 meilleurs :")
for i in range(0, 10):
    print(all_combinations[i])

print()

print("10 pires :")
for i in range(10, 0, -1):
    print(all_combinations[-i])

print("longueur du meilleur: ")
print(len(all_combinations[0][0]))
print("Le grand gagnant est:")
print(all_combinations[0])
print()
print("total_duration:")
print(elapsed_time_formatted(start_all))
