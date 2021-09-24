import time

import tablib


def elapsed_time_formatted(begin_time):
    """
    Calculates difference between begin_time and actual time,
    and formats it in HH:MM:SS:ms.
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


def shares_cost_sum(dataset):
    cost_sum = 0
    for data in dataset:
        cost_sum += data[1]
    return cost_sum


def best_combination_dynamic(dataset, max_cost):
    max_cost_in_cents = max_cost * 100
    dataset_length = len(dataset)
    matrix = [[0 for x in range(max_cost_in_cents + 1)] for x in range(dataset_length + 1)]
    for action in range(1, dataset_length + 1):
        for size in range(1, max_cost_in_cents + 1):
            if dataset[action - 1][1] <= size:
                matrix[action][size] = max(dataset[action - 1][3] + matrix[action - 1][size - dataset[action - 1][1]], matrix[action - 1][size])
            else:
                matrix[action][size] = matrix[action - 1][size]

    best_combination = []
    budget_remaining = max_cost_in_cents
    while budget_remaining >= 0 and dataset_length >= 0:
        if matrix[dataset_length][budget_remaining] == matrix[dataset_length - 1][budget_remaining - dataset[dataset_length - 1][1]] + dataset[dataset_length - 1][3]:
            best_combination.append(dataset[dataset_length - 1])
            budget_remaining -= dataset[dataset_length - 1][1]
        dataset_length -= 1

    return matrix[-1][-1], best_combination


def main():
    start = time.perf_counter()
    base_dataset = open_convert_and_clean_csv('dataset2_Python+P7.csv')
    computable_dataset = add_roi_to_dataset(convert_dataset_to_cents(base_dataset))
    best_roi, combination = best_combination_dynamic(computable_dataset, 500)
    best_roi /= 100
    combination.sort(key=lambda action: action[3], reverse=True)
    shares_cost = shares_cost_sum(combination)/100
    final_combination = convert_dataset_to_euros(combination)

    print(f"Length of dataset: {len(computable_dataset)}")
    print(f"Duration of Analysis: {elapsed_time_formatted(start)}")
    print()
    print(f"Best Return on investment after 2 years: {best_roi} €")
    print(f"Best set of shares ordered by performance = {final_combination}")
    print(f"Number of shares to buy : {len(final_combination)}")
    print(f"Total cost: {shares_cost} €")


if __name__ == "__main__":
    main()
