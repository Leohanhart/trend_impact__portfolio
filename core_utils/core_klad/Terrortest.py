# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 17:41:41 2023

@author: Gebruiker
"""

import pickle
import os
import inspect


def save_variables_to_pickle(filename, **kwargs):
    # Get the caller's local variables
    caller_locals = inspect.currentframe().f_back.f_locals

    # Filter out the variables that are not in kwargs
    variables = {
        var: caller_locals[var] for var in kwargs if var in caller_locals
    }

    # Save the variables to a pickle file
    with open(filename, "wb") as file:
        pickle.dump(variables, file)


def restore_variables_from_pickle(filename):
    # Load the variables from the picskle file
    with open(filename, "rb") as file:
        variables = pickle.load(file)

    # Get the caller's local variables
    caller_locals = inspect.currentframe().f_back.f_locals

    # Update the caller's local variables with the loaded variables
    caller_locals.update(variables)


def delete_pickle_file(filename):
    # Delete the pickle file
    if os.path.exists(filename):
        os.remove(filename)


def test():

    items = [1, 2, 3]
    tickers_in = ["AAPL", "GOOGL", "MSFT"]
    tickers_list_name = "MyTickers"
    min_amount_tickers = 10
    max_rotations = 5
    max_stocks = 20
    min_sharp_ratio = 0.8

    # Save the variables to a pickle file
    filename = "variables.pickle"
    save_variables_to_pickle(
        filename,
        items=items,
        tickers_in=tickers_in,
        tickers_list_name=tickers_list_name,
        min_amount_tickers=min_amount_tickers,
        max_rotations=max_rotations,
        max_stocks=max_stocks,
        min_sharp_ratio=min_sharp_ratio,
    )

    # Modify the variables
    items.append(4)
    tickers_in.append("AMZN")
    min_amount_tickers = 5

    # Print the modified variables
    print(items)
    print(tickers_in)
    print(min_amount_tickers)

    # Restore the variables from the pickle file
    restore_variables_from_pickle(filename)

    # Print the restored variables
    print(items)
    print(tickers_in)
    print(min_amount_tickers)

    # Delete the pickle file
    # delete_pickle_file(filename)


if __name__ == "__main__":
    test()
