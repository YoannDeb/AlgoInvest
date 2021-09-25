import argparse
from itertools import combinations
import time
import tablib


def set_arg():
    """
    Initiate argparser argument "--databasefile" to change database file name.
    :return: The new database's filename, or None if no argument were given.
    """
    parser = argparse.ArgumentParser(
        description="Use a data CSV file and/or max investment amount different "
                    "from the default one ('dataset0_training.csv' and '500€')."
    )
    parser.add_argument("-d", "--databasefile", help="name of the data CSV file to use")
    parser.add_argument("-i", "--investment", help="max investment in euros")
    args = parser.parse_args()
    return args.databasefile, args.investment


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
    price_list2.sort(key=lambda x: x[1])
    return price_list2


def calculate_max_size_wallet_length(price_list_ordered, max_cost):
    max_size_wallet = []
    total_cost2 = 0
    for action in price_list_ordered:
        total_cost2 += action[1]
        if total_cost2 > max_cost:
            total_cost2 -= action[1]
        else:
            max_size_wallet.append(action)
    return len(max_size_wallet)


def calculate_min_size_wallet_length(price_list_ordered, max_cost):
    price_list_ordered.reverse()
    min_size_wallet = []
    total_cost2 = 0
    for action in price_list_ordered:
        total_cost2 += action[1]
        if total_cost2 > max_cost:
            total_cost2 -= action[1]
        else:
            min_size_wallet.append(action)
    price_list_ordered.reverse()
    return len(min_size_wallet)


def open_convert_and_clean_csv(csv_data_file):
    imported_data = tablib.Dataset().load(open(csv_data_file).read())
    dataset = []
    for row in imported_data:
        if float(row[1]) > 0 and float(row[2]) > 0:
            dataset.append((row[0], float(row[1]), int(row[2])))
    return dataset


def main():
    # Retrieve csv_file name and max_cost from argument passed in console:
    arg_csv_file, arg_max_investment = set_arg()
    if arg_csv_file:
        csv_file = arg_csv_file
    else:
        csv_file = 'dataset0_training.csv'
    if arg_max_investment:
        max_cost = float(arg_max_investment)
    else:
        max_cost = 500.00

    base_dataset = open_convert_and_clean_csv(csv_file)

    start_all = time.perf_counter()

    sorted_list = sorted_price_list(base_dataset)
    max_list_size = calculate_max_size_wallet_length(sorted_list, max_cost)
    min_list_size = calculate_min_size_wallet_length(sorted_list, max_cost)

    print()
    print(f"Processing with file '{csv_file}' containing {len(base_dataset)} shares...")
    print(f"Maximum investment: {max_cost}€")
    print(f"min found : {min_list_size}")
    print(f"max found : {max_list_size}")
    print("Please wait...")

    all_combinations_with_cost_and_roi = []
    for i in range(min_list_size, (max_list_size + 1)):
        for combination in combinations(base_dataset, i):
            total_roi = 0.0
            total_cost = 0.0
            # Calculate global ROI of wallet
            for element in combination:
                total_cost += element[1]
                total_roi += (element[1]*element[2])/100
            # Append it if it is in the investment limit
            if total_cost <= max_cost:
                combination_with_cost_and_roi = (combination, total_cost, total_roi)
                all_combinations_with_cost_and_roi.append(combination_with_cost_and_roi)
        print(f"{i} length terminated")
        print(f"Duration of Analysis: {elapsed_time_formatted(start_all)}")

    # Sort results by descending ROI
    all_combinations_with_cost_and_roi.sort(key=lambda x: x[2], reverse=True)

    best_combination = list(all_combinations_with_cost_and_roi[0][0])

    best_combination.sort(key=lambda x: x[2], reverse=True)
    print(all_combinations_with_cost_and_roi[0][0])
    # Printing results:
    print()
    print(f"Length of dataset: {len(base_dataset)}")
    print(f"Duration of Analysis: {elapsed_time_formatted(start_all)}")
    print()
    print(f"Best Return on investment after 2 years: {all_combinations_with_cost_and_roi[0][2]}€")
    print(f"Number of shares to buy : {len(all_combinations_with_cost_and_roi[0][0])}")
    print(f"Total cost: {all_combinations_with_cost_and_roi[0][1]}€")
    print()
    print(f"Best set of shares ordered by performance: ")
    for share in best_combination:
        print(f"{share[0]} | Price: {share[1]}€ | profit: {share[2]}%")
    print()


if __name__ == "__main__":
    main()
