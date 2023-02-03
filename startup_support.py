# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 11:34:06 2023

@author: Gebruiker
"""
from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
import numpy as np


def check_if_today_is_businessday():
    """
    Check if today is first business day of the month. 

    Returns
    -------
    bool
        DESCRIPTION.

    """

    dt = datetime.now()
    td = timedelta(days=30)
    # your calculated date
    my_date = dt + td

    staturedays = pd.date_range(dt.strftime(
        "%d-%m-%Y"), my_date.strftime("%d-%m-%Y"),
        freq='W-SAT')

    sundays = pd.date_range(dt.strftime(
        "%d-%m-%Y"), my_date.strftime("%d-%m-%Y"),
        freq='W-SUN')

    if np.datetime64(dt, 'D') in staturedays or np.datetime64(dt, 'D') in sundays:
        return False
    else:
        return True


def check_if_today_is_first_the_month():
    """
    Check if today is first business day of the month. 

    Returns
    -------
    bool
        DESCRIPTION.

    """

    dt = datetime.now()
    td = timedelta(days=5)
    # your calculated date
    my_date = dt + td

    first_business_days = pd.date_range(dt.strftime(
        "%d-%m-%Y"), my_date.strftime("%d-%m-%Y"),
    )  # freq='BMS')

    if np.datetime64(dt, 'D') in first_business_days:
        return True
    else:
        return False


def check_if_today_is_first_the_quarter():
    """

    Check if today is first business day of the quarter. 

    Returns
    -------
    bool
        DESCRIPTION.

    """

    dt = datetime.now()
    td = timedelta(days=365)
    # your calculated date
    my_date = dt + td

    first_business_days = pd.date_range(dt.strftime(
        "%d-%m-%Y"), my_date.strftime("%d-%m-%Y"), freq='BMS')

    if np.datetime64(dt, 'D') in first_business_days:
        return True
    else:
        return False
