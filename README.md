# AlgoInvest
Training program


## bruteforce:
### Principle:
We first found the maximum and minimum length possible with constraints (ie buying the cheapest the most expensive shares within the investment limit)

Then for each possible length, we found all possible combinations.
We then calculate the cost and profit of each combination.
If the cost is less or equal to the max_investment, we keep this combination with it's cost and profit.

Once all possible combinations have been calculated and tested, we sort by descending profit.

The best one is the optimal solution.

All solutions within the constraint have been tested.

### Complexity:
n = number of shares
Temporal complexity : O(2^n)
Spatial complexity : O(1)

## optimized:
### Principle:
Adapting knapsack problem with shares. Capacity is investment limit. Weight is price of an action. Value is ROI (Return on Investment).

All fiduciary values are converted in cents to avoid floats.

First a matrix is initialized at 0 everywhere, of size : length of the dataset * max investment (in cents).

For every share, for each investment size, is found if the share alone will first fit in the size, if so, if it's ROI is better than the previous solution without it.

Put the best ROI between the two in the matrix.

At the end of the matrix will be the ROI of the best possible "fit".

An algorithm then can find the chosen shares by backtracking the matrix.

We finally, after euros conversion have the best combination possible and the best ROI.

### Complexity:
I = max investment (in cents)
n = number of shares 
Temporal complexity: O(I*n)
Spatial complexity: O(I*n)

