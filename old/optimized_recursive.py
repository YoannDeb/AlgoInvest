import argparse
import time
import tablib


def set_arg():
    """
    Initiate argparser argument "--databasefile" to change database file name.
    :return: The new database's filename, or None if no argument were given.
    """
    parser = argparse.ArgumentParser(
        description="Use a data CSV file and/or max investment amount different "
                    "from the default one ('dataset1_Python+P7.csv' and '500€')."
    )
    parser.add_argument("-d", "--databasefile", help="name of the data CSV file to use")
    parser.add_argument("-i", "--investment", help="max investment in euros")
    args = parser.parse_args()
    return args.databasefile, args.investment


def elapsed_time_formatted(begin_time):
    """
    Calculates difference between begin_time and actual time,
    and formats it in HH:MM:SS:ms.
    :param begin_time: time we want to compare with, in seconds.
    """
    return time.strftime(
        "%H:%M:%S", (time.gmtime(time.perf_counter() - begin_time))
    )


def open_convert_and_clean_csv(csv_data_file: str):
    imported_data = tablib.Dataset().load(open(csv_data_file).read())
    dataset = []
    for row in imported_data:
        if float(row[1]) > 0 and float(row[2]) > 0:
            dataset.append((row[0], float(row[1]), float(row[2])))
    return dataset


def convert_dataset_to_cents(dataset):
    dataset_in_cents = []
    for data in dataset:
        dataset_in_cents.append((data[0], int(data[1] * 100), data[2]))
    return dataset_in_cents


def convert_dataset_to_euros(dataset):
    dataset_in_euros = []
    for data in dataset:
        dataset_in_euros.append((data[0], float(data[1]/100), data[2], data[3]/100))
    return dataset_in_euros


def add_roi_to_dataset(dataset):
    return [(data[0], data[1], data[2], (data[1] * data[2]) / 100) for data in dataset]


def best_combination_dynamic(dataset, max_cost):
    # Finding best ROI (return On Investment):
    max_cost_in_cents = int(max_cost * 100)
    dataset_length = len(dataset)
    matrix = [[0 for x in range(max_cost_in_cents + 1)] for x in range(dataset_length + 1)]
    for action in range(1, dataset_length + 1):
        for size in range(1, max_cost_in_cents + 1):
            if dataset[action - 1][1] <= size:
                matrix[action][size] = max(dataset[action - 1][3] + matrix[action - 1][size - dataset[action - 1][1]], matrix[action - 1][size])
            else:
                matrix[action][size] = matrix[action - 1][size]

    # Retrieving best combination from matrix:
    best_combination = []
    budget_remaining = max_cost_in_cents
    while budget_remaining >= 0 and dataset_length >= 0:
        if matrix[dataset_length][budget_remaining] == matrix[dataset_length - 1][budget_remaining - dataset[dataset_length - 1][1]] + dataset[dataset_length - 1][3]:
            best_combination.append(dataset[dataset_length - 1])
            budget_remaining -= dataset[dataset_length - 1][1]
        dataset_length -= 1

    return matrix[-1][-1], best_combination


def recursive_solver(max_cost, prices, rois, list_size):
    if list_size == 0 or max_cost == 0:
        return 0

    if memo[list_size][max_cost] != -1:
        return memo[list_size][max_cost]

    if prices[list_size - 1] <= max_cost:
        memo[list_size][max_cost] = max(rois[list_size - 1] + recursive_solver(max_cost - prices[list_size - 1], prices, rois, list_size - 1),
                                        recursive_solver(max_cost, prices, rois, list_size - 1))
        return memo[list_size][max_cost]
    elif prices[list_size - 1] > max_cost:
        memo[list_size][max_cost] = recursive_solver(max_cost, prices, rois, list_size - 1)
        return memo[list_size][max_cost]


def get_cost_of_combination(combination):
    cost = 0
    for share in combination:
        cost += share[1]
    return cost


def get_roi_of_combination(combination):
    roi = 0
    for share in combination:
        roi += share[3]
    return roi


def main():
    # Retrieve csv_file name an max_cost from argument passed in console:
    arg_csv_file, arg_max_investment = set_arg()
    if arg_csv_file:
        csv_file = arg_csv_file
    else:
        csv_file = 'dataset0_training.csv'
    if arg_max_investment:
        max_cost = float(arg_max_investment)
    else:
        max_cost = 500.00

    # Retrieve dataset:
    base_dataset = open_convert_and_clean_csv(csv_file)

    # Retrieve solution:
    start = time.perf_counter()
    print()
    print(f"Processing with file '{csv_file}' containing {len(base_dataset)} shares...")
    print(f"Maximum investment: {max_cost}€")
    print("Please wait...")
    computable_dataset = add_roi_to_dataset(convert_dataset_to_cents(base_dataset))
    prices = [i[1] for i in computable_dataset]
    rois = [i[3] for i in computable_dataset]
    max_cost = int(max_cost * 100)
    global memo
    memo = [[-1 for i in range(max_cost + 1)] for j in range(len(computable_dataset) + 1)]
    solution = recursive_solver(max_cost, prices, rois, len(computable_dataset))
    # combination = best_combination_linear(computable_dataset, max_cost)
    # best_roi = get_roi_of_combination(combination)

    # best_roi, combination = best_combination_dynamic(computable_dataset, max_cost)
    #
    # Formatting results:
    # combination.sort(key=lambda x: x[2], reverse=True)
    # final_combination = convert_dataset_to_euros(combination)
    # shares_cost = get_cost_of_combination(combination)

    # Printing results:
    print()
    print(f"Length of dataset: {len(computable_dataset)}")
    print(f"Duration of Analysis: {elapsed_time_formatted(start)}")
    print(f"Best *Return On Investment: {round(solution/100, 2)}")
    # print(f"Best Return on investment after 2 years: {round(best_roi, 2)}€")
    # print(f"Number of shares to buy : {len(combination)}")
    # print(f"Total cost: {shares_cost}€")
    # print()
    # print(f"Best set of shares ordered by performance: ")
    # for share in combination:
    #     print(f"{share[0]} | Price: {share[1]}€ | profit: {share[2]}%")
    # print()


if __name__ == "__main__":
    memo = []
    main()
