# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 20:32:14 2022

@author: Gebruiker
"""

from tqdm import tqdm

import os, sys

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def test_this_function():
    print("this is who we do")

for i in tqdm(range(1,10000)):
    with HiddenPrints():
      test_this_function()