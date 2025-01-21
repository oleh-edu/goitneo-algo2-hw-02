#!/usr/bin/env python

from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds the best way to cut through memoization

    Args:
        length: the length of the rod
        prices: a list of prices, where prices[i] is the price of a rod of length i+1

    Returns:
        Dict with maximum profit and a list of cuts
    """
    memo = {}

    def helper(n):
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = 0
        best_cuts = []

        for i in range(1, n + 1):
            profit, cuts = helper(n - i)
            profit += prices[i - 1]

            if profit > max_profit:
                max_profit = profit
                best_cuts = cuts + [i]

        memo[n] = (max_profit, best_cuts)
        return memo[n]

    max_profit, cuts = helper(length)
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1 if cuts else 0
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut through tabs

    Args:
        length: the length of the rod
        prices: a list of prices, where prices[i] is the price of a rod of length i+1

    Returns:
        Dict with the maximum profit and a list of cuts
    """
    dp = [0] * (length + 1)
    cuts = [0] * (length + 1)

    for i in range(1, length + 1):
        max_profit = 0
        for j in range(1, i + 1):
            if prices[j - 1] + dp[i - j] > max_profit:
                max_profit = prices[j - 1] + dp[i - j]
                cuts[i] = j
        dp[i] = max_profit

    n = length
    result_cuts = []
    while n > 0:
        result_cuts.append(cuts[n])
        n -= cuts[n]

    return {
        "max_profit": dp[length],
        "cuts": result_cuts,
        "number_of_cuts": len(result_cuts) - 1
    }

def run_tests():
    """Function to run all tests"""
    test_cases = [
        # Test 1: Base case
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "The basic case"
        },
        # Test 2: It is optimal not to cut
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Optimally do not cut"
        },
        # Test 3: All cuts are 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Uniform cuts"
        }
    ]

    for test in test_cases:
        print(f"\n[test] Test: {test['name']}")
        print(f"Length of the rod: {test['length']}")
        print(f"Prices: {test['prices']}")

        # Testing memoization
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\n[result] The result of memoization:")
        print(f"Maximum profit: {memo_result['max_profit']}")
        print(f"Cuts: {memo_result['cuts']}")
        print(f"Number of cuts: {memo_result['number_of_cuts']}")

        # Testing tabulation
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\n[result] Tabulation result:")
        print(f"Maximum profit: {table_result['max_profit']}")
        print(f"Cuts: {table_result['cuts']}")
        print(f"Number of cuts: {table_result['number_of_cuts']}")

        print("\n[done] The test was successful!")

if __name__ == "__main__":
    run_tests()
