# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 13:29:14 2023

@author: Gebruiker
"""

import os


def delete_lock_file(lock_file_path):
    if os.path.exists(lock_file_path):
        try:
            os.remove(lock_file_path)
            print(f"'{lock_file_path}' deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting '{lock_file_path}': {e}")
    else:
        print(f"'{lock_file_path}' does not exist.")


if __name__ == "__main__":
    lock_file_path = "process.lock"
    delete_lock_file(lock_file_path)
