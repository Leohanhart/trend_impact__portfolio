# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 11:30:44 2022

@author: Gebruiker
"""


def Convert(lst):
    
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 1)}
    
    return res_dct
         
# Driver code
def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d

global lst

lst = [{'Date': '12-12-1980', 'Open': 0.1283479928970337, 'High': 0.1289059966802597, 'Low': 0.1283479928970337, 'Close': 0.1283479928970337, 'Adj Close': 0.10017845034599304, 'Volume': 469033600, 'Change': 0.0},
       {'Date': '12-12-1980', 'Open': 0.1283479928970337, 'High': 0.1289059966802597, 'Low': 0.1283479928970337, 'Close': 0.1283479928970337, 'Adj Close': 0.10017845034599304, 'Volume': 469033600, 'Change': 0.0},
       {'Date': '12-12-1980', 'Open': 0.1283479928970337, 'High': 0.1289059966802597, 'Low': 0.1283479928970337, 'Close': 0.1283479928970337, 'Adj Close': 0.10017845034599304, 'Volume': 469033600, 'Change': 0.0},
       {'Date': '12-12-1980', 'Open': 0.1283479928970337, 'High': 0.1289059966802597, 'Low': 0.1283479928970337, 'Close': 0.1283479928970337, 'Adj Close': 0.10017845034599304, 'Volume': 469033600, 'Change': 0.0},
       {'Date': '12-12-1980', 'Open': 0.1283479928970337, 'High': 0.1289059966802597, 'Low': 0.1283479928970337, 'Close': 0.1283479928970337, 'Adj Close': 0.10017845034599304, 'Volume': 469033600, 'Change': 0.0},
       {'Date': '12-12-1980', 'Open': 0.1283479928970337, 'High': 0.1289059966802597, 'Low': 0.1283479928970337, 'Close': 0.1283479928970337, 'Adj Close': 0.10017845034599304, 'Volume': 469033600, 'Change': 0.0},
       {'Date': '12-12-1980', 'Open': 0.1283479928970337, 'High': 0.1289059966802597, 'Low': 0.1283479928970337, 'Close': 0.1283479928970337, 'Adj Close': 0.10017845034599304, 'Volume': 469033600, 'Change': 0.0},
       {'Date': '12-12-1980', 'Open': 0.1283479928970337, 'High': 0.1289059966802597, 'Low': 0.1283479928970337, 'Close': 0.1283479928970337, 'Adj Close': 0.10017845034599304, 'Volume': 469033600, 'Change': 0.0},
       {'Date': '12-12-1980', 'Open': 0.1283479928970337, 'High': 0.1289059966802597, 'Low': 0.1283479928970337, 'Close': 0.1283479928970337, 'Adj Close': 0.10017845034599304, 'Volume': 469033600, 'Change': 0.0}
       ]

global x 

def GetADict(e):
    
    x = {}
    
    