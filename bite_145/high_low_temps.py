from collections import namedtuple

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
    df.Data_Value = df.Data_Value.astype("int64")
    df.Date = pd.to_datetime(df.Date)
    df.set_index(["Date"], inplace=True)

    df = df["2005":"2015"]
    df = df.drop([d for d in df.index if d.month == 2 and d.day == 29])

    dates = df["2015"].index.unique()

    highest = None
    lowest = None
    for date in dates:
        high_ = (
            df.loc[
                (df.index.month == date.month)
                & (df.index.day == date.day)
                & (df.Element == "TMAX")
            ]
            .sort_values("Data_Value", ascending=False)
            .head(1)
        )

        low_ = (
            df.loc[
                (df.index.month == date.month)
                & (df.index.day == date.day)
                & (df.Element == "TMIN")
            ]
            .sort_values("Data_Value", ascending=True)
            .head(1)
        )

        if high_.index.year == 2015:
            if highest is None or high_["Data_Value"][0] > highest["Data_Value"][0]:
                highest = high_

        if low_.index.year == 2015:
            if lowest is None or low_["Data_Value"][0] < lowest["Data_Value"][0]:
                lowest = low_

    high = STATION(highest.ID[0], highest.index[0], highest.Data_Value[0] / 10)
    low = STATION(lowest.ID[0], lowest.index[0], lowest.Data_Value[0] / 10)

    return high, low
