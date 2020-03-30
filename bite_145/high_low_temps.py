from collections import namedtuple
from datetime import date

import pandas as pd

DATA_FILE = "http://projects.bobbelderbos.com/pcc/weather-ann-arbor.csv"
STATION = namedtuple("Station", "ID Date Value")


def high_low_record_breakers_for_2015():
    """Extract the high and low record breaking temperatures for 2015

    The expected value will be a tuple with the highest and lowest record
    breaking temperatures for 2015 as compared to the temperature data
    provided.

    NOTE:
    The date values should not have any timestamps, should be a
    datetime.date() object. The temperatures in the dataset are in tenths
    of degrees Celsius, so you must divide them by 10

    Possible way to tackle this challenge:

    1. Create a DataFrame from the DATA_FILE dataset.

    2. Manipulate the data to extract the following:
       * Extract highest temperatures for each day / station pair between 2005-2015
       * Extract lowest temperatures for each  day / station  between 2005-2015
       * Remove February 29th from the dataset to work with only 365 days

    3. Separate data into two separate DataFrames:
       * high/low temperatures between 2005-2014
       * high/low temperatures for 2015

    4. Iterate over the 2005-2014 data and compare to the 2015 data:
       * For any temperature that is higher/lower in 2015 extract ID,
         Date, Value

    5. From the record breakers in 2015, extract the high/low of all the
       temperatures
       * Return those as STATION namedtuples, (high_2015, low_2015)
    """
    # 1
    df = pd.read_csv(DATA_FILE)

    # 2
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index(['Date'])

    df = df['2005':'2015']
    df = df.drop([
        d for d in df.index if d.month == 2 and d.day == 29
    ])

    high = df[df.Element == "TMAX"]
    lows = df[df.Element == "TMIN"]

    high_2005_2014 = high['2005':'2014']
    lows_2005_2014 = lows['2005':'2014']
    high_2015 = high['2015']
    lows_2015 = lows['2015']

    high_low_2015 = find_breakers(high_2005_2014, high_2015, lows_2005_2014, lows_2015)

    return high_low_2015


def find_breakers(h205214, h215, l205214, l215):
    records = []

    for date_ in h215.index:
        high_data = h205214.loc[
            (h205214.index.month == date_.month) &
            (h205214.index.day == date_.day)
        ]
        low_data = l205214.loc[
            (l205214.index.month == date_.month) &
            (h205214.index.day == date_.day)
        ]

        for station_ in h215.ID[date_].unique():


