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
    df = df.set_index(["Date"])

    df = df["2005":"2015"]

    df = df.drop([d for d in df.index if d.month == 2 and d.day == 29])

    high = df[df.Element == "TMAX"]
    lows = df[df.Element == "TMIN"]
    del df

    high_2005_2014 = high["2005":"2014"]
    high_2015 = high["2015"]
    del high

    lows_2005_2014 = lows["2005":"2014"]
    lows_2015 = lows["2015"]
    del lows

    highs = list()
    for date_ in high_2015.index.unique():
        daily_df = high_2005_2014.loc[
            (high_2005_2014.index.month == date_.month) & (high_2005_2014.index.day == date_.day)
            ]
        daily_2015_df = high_2015.loc[high_2015.index == date_.strftime('%Y-%m-%d')]
        daily_df.reset_index('Date', inplace=True)
        daily_2015_df.reset_index('Date', inplace=True)
        joined_df = pd.merge(daily_df, daily_2015_df, on='ID')
        grouped = joined_df.groupby(['ID']).max()
        for id_ in grouped.index:
            if grouped.Data_Value_x[id_] < grouped.Data_Value_y[id_]:
                highs.append(
                    STATION(
                        id_,
                        date_.date(),
                        grouped.Data_Value_y[id_] / 10,
                    )
                )

    del high_2005_2014
    del high_2015

    lows = list()
    for date_ in lows_2015.index.unique():
        daily_df = lows_2005_2014.loc[
            (lows_2005_2014.index.month == date_.month) & (lows_2005_2014.index.day == date_.day)
            ]
        daily_2015_df = lows_2015.loc[lows_2015.index == date_.strftime('%Y-%m-%d')]
        daily_df.reset_index('Date', inplace=True)
        daily_2015_df.reset_index('Date', inplace=True)
        joined_df = pd.merge(daily_df, daily_2015_df, on='ID')
        grouped = joined_df.groupby(['ID']).min()
        for id_ in grouped.index:
            if grouped.Data_Value_x[id_] > grouped.Data_Value_y[id_]:
                lows.append(
                    STATION(
                        id_,
                        date_.date(),
                        grouped.Data_Value_y[id_] / 10,
                    )
                )
    del lows_2005_2014
    del lows_2015

    high = STATION(" ", " ", 0)
    low = STATION(" ", " ", 100)

    for high_ in highs:
        if high_.Value > high.Value:
            high = high_

    for low_ in lows:
        if low_.Value < low.Value:
            low = low_

    return high, low
