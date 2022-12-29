# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 23:21:49 2022

@author: Gebruiker
"""
import os, sys
from os import system, name


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def clear():
   # for windows
   if name == 'nt':
      _ = system('cls')

   # for mac and linux
   else:
       _ = system('clear')
   
   
