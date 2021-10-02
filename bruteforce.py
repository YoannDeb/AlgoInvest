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


def elapsed_time_formatted(begin_time):
    """
    Calculates difference between begin_time and actual time,
    and formats it in HH:MM:SS.
    :param begin_time: time we want to compare with, in seconds.
    """
    return time.strftime(
        "%H:%M:%S", (time.gmtime(time.perf_counter() - begin_time))
    )


def open_convert_and_clean_csv(csv_data_file):
    imported_data = tablib.Dataset().load(open(csv_data_file).read())
    dataset = []
    for row in imported_data:
        if float(row[1]) > 0 and float(row[2]) > 0:
            dataset.append((row[0], float(row[1]), int(row[2])))
    return dataset


def convert_dataset_to_cents(dataset):
    dataset_in_cents = []
    for data in dataset:
        dataset_in_cents.append((data[0], int(data[1] * 100), data[2]))
    return dataset_in_cents


def convert_combination_in_euros(combination):
    combination_in_euros = [[], None, None]
    # for share in combination[0]:
    #     combination_in_euros[0].append((share[0], (share[1])/100, share[2]))
    combination_in_euros[0] = [(share[0], (share[1])/100, share[2]) for share in combination[0]]
    combination_in_euros[1] = combination[1]/100
    combination_in_euros[2] = combination[2]/100
    return combination_in_euros


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

    max_cost_in_cents = int(max_cost * 100)
    dataset_in_cents = convert_dataset_to_cents(base_dataset)

    print()
    print(f"Processing with file '{csv_file}' containing {len(base_dataset)} shares...")
    print(f"Maximum investment: {max_cost}€")
    print("Please wait...")

    best_combination = [[0], 0, 0]
    for i in range(len(dataset_in_cents)):
        for combination in combinations(dataset_in_cents, i):
            total_roi = 0.0
            total_cost = 0.0
            # Calculate global ROI of wallet
            for element in combination:
                total_cost += element[1]
                total_roi += (element[1]*element[2])/100
            # Append it if it is in the investment limit
            if total_cost <= max_cost_in_cents and total_roi > best_combination[2]:
                best_combination = [combination, total_cost, total_roi]
        print(f"{i} length terminated")
        print(f"Duration of Analysis: {elapsed_time_formatted(start_all)}")

    best_combination = convert_combination_in_euros(best_combination)
    best_combination[0].sort(key=lambda x: x[2], reverse=True)

    # Printing results:
    print()
    print(f"Length of dataset: {len(base_dataset)}")
    print(f"Duration of Analysis: {elapsed_time_formatted(start_all)}")
    print()
    print(f"Best Return on investment after 2 years: {best_combination[2]}€")
    print(f"Number of shares to buy : {len(best_combination[0])}")
    print(f"Total cost: {best_combination[1]}€")
    print()
    print(f"Best set of shares ordered by performance: ")
    for share in best_combination[0]:
        print(f"{share[0]} | Price: {share[1]}€ | profit: {share[2]}%")
    print()


if __name__ == "__main__":
    main()
