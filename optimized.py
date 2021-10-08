import argparse
import time
import tablib


def set_arg():
    """
    Initiate argparser arguments :
    - "--databasefile" to change database file name
    - "--investment" to change max investment.
    :return: The new database's filename and the new investment, or None for each if no argument were given.
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


def open_convert_and_clean_csv(csv_data_file):
    """
    Just opens a csv data file and returns a list of tuples.
    One tuple is composed by the name of the share, it's cost in euros and it's profit rate % after two years.
    :param csv_data_file: Name of the csv file.
    :return: A list of tuples. One tuple for one share.
    """
    imported_data = tablib.Dataset().load(open(csv_data_file).read())
    dataset = []
    for row in imported_data:
        if float(row[1]) > 0 and float(row[2]) > 0:
            dataset.append((row[0], float(row[1]), float(row[2])))
    return dataset


def convert_dataset_to_cents(dataset):
    """
    Converts prices of all elements of a list of shares from euros to cents.
    :param dataset: A list of shares in euros.
    :return: A list of shares in cents.
    """
    dataset_in_cents = []
    for data in dataset:
        dataset_in_cents.append((data[0], int(data[1] * 100), data[2]))
    return dataset_in_cents


def convert_dataset_to_euros(dataset):
    """
    Converts a dataset in euros.
    :param dataset: A list of shares. Each share is a tuple composed of the name,
        the price, the profit rate and the share's return on investment.
    :return: A shares list in euros.
    """
    dataset_in_euros = []
    for data in dataset:
        dataset_in_euros.append((data[0], float(data[1]/100), data[2], data[3]/100))
    return dataset_in_euros


def add_roi_to_dataset(dataset):
    """
    Adds return on investment to the dataset for each share, calculated from price and profit rate.
    :param dataset: A list of shares. Each share is a tuple composed of the name,
        the price, and the profit rate.
    :return: A list of shares. Each share is a tuple composed of the name,
        the price, the profit rate and the return on investment.
    """
    return [(data[0], data[1], data[2], (data[1] * data[2]) / 100) for data in dataset]


def calculate_shares_cost_sum(dataset):
    """
    Takes a list of shares and returns the total cost of all shares in that list.
    :param dataset: A list of shares.
    :return: The total cost of all shares.
    """
    cost_sum = 0
    for data in dataset:
        cost_sum += data[1]
    return cost_sum


def best_combination_dynamic(dataset, max_investment):
    """
    Dynamic algorithm handler, inspired from knapsack problem.
    Capacity is investment limit. Weight is price of an action. Value is ROI (Return on Investment).
    All fiduciary values needs to be in cents to avoid floats.
    First a matrix is initialized with 0 everywhere, of size : length of the dataset * max investment (in cents).
    For every share, then for each investment size, is found if the share alone will first fit in the size.
    If so, checks if it's ROI is better than the previous solution without it.
    Puts the best ROI between the two in the matrix at the current share and investment coordinates.
    When all is processed, the end of the matrix will contain the best ROI of the best possible combination.
    The second part of the algorithm finds the shares chosen by backtracking the matrix.
    :param dataset: A list of shares. Each share is a tuple composed of the name,
        the price (in cents), the profit rate and the return on investment (in cents).
    :param max_investment: Max investment possible to buy actions, in euros (converted in cents in the function)
    :return: Best ROI and best combination.
    """
    # Finding best ROI (return On Investment):
    max_investment_in_cents = int(max_investment * 100)
    dataset_length = len(dataset)
    matrix = [[0 for x in range(max_investment_in_cents + 1)] for x in range(dataset_length + 1)]
    for share in range(1, dataset_length + 1):
        for budget in range(1, max_investment_in_cents + 1):
            current_share = dataset[share - 1]
            if current_share[1] <= budget:
                matrix[share][budget] = max(current_share[3] + matrix[share - 1][budget - current_share[1]],
                                            matrix[share - 1][budget])
            else:
                matrix[share][budget] = matrix[share - 1][budget]

    # Retrieving best combination from matrix:
    best_combination = []
    budget_remaining = max_investment_in_cents
    while budget_remaining >= 0 and dataset_length >= 0:
        current_share = dataset[dataset_length - 1]
        if matrix[dataset_length][budget_remaining] == \
                matrix[dataset_length - 1][budget_remaining - current_share[1]]\
                + current_share[3]:
            best_combination.append(current_share)
            budget_remaining -= current_share[1]
        dataset_length -= 1

    return matrix[-1][-1], best_combination


def main():
    """
    Main function.
    Takes a datafile and max investment from args, and gives the best shares selection
        and return on investment within the max investment limit.
    Conversion in cents for more precision in calculus.
    Uses best_combination_dynamic() function as solver algorithm.
    At the end the best combination is reconverted back in euros, and sorted by profit rate.
    Results are printed in console, including duration of analysis, total cost, total return on investment,
        number of shares to buy and finally the list of all shares to buy with details.
    """
    # Retrieve csv_file name an max_investment from argument passed in console:
    arg_csv_file, arg_max_investment = set_arg()
    if arg_csv_file:
        csv_file = arg_csv_file
    else:
        csv_file = 'dataset1_Python+P7.csv'
    if arg_max_investment:
        max_investment = float(arg_max_investment)
    else:
        max_investment = 500.00

    # Retrieve dataset:
    base_dataset = open_convert_and_clean_csv(csv_file)

    # Retrieve solution:
    start = time.perf_counter()
    print()
    print(f"Processing with file '{csv_file}' containing {len(base_dataset)} shares...")
    print(f"Maximum investment: {max_investment}€")
    print("Please wait...")
    computable_dataset = add_roi_to_dataset(convert_dataset_to_cents(base_dataset))
    best_roi, combination = best_combination_dynamic(computable_dataset, max_investment)

    # Formatting results:
    combination.sort(key=lambda x: x[2], reverse=True)
    combination_in_euros = convert_dataset_to_euros(combination)
    best_roi /= 100
    # Following calculus is done on cent prices (combination) to avoid approximations with floats
    shares_cost = calculate_shares_cost_sum(combination) / 100

    # Printing results:
    print()
    print(f"Length of dataset: {len(computable_dataset)}")
    print(f"Duration of Analysis: {elapsed_time_formatted(start)}")
    print()
    print(f"Best Return on investment after 2 years: {round(best_roi, 2)}€")
    print(f"Number of shares to buy : {len(combination_in_euros)}")
    print(f"Total cost: {round(shares_cost, 2)}€")
    print()
    print(f"Best combination of shares ordered by performance: ")
    for share in combination_in_euros:
        print(f"{share[0]} | Price: {share[1]}€ | profit: {share[2]}%")
    print()


if __name__ == "__main__":
    main()
