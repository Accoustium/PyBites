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

    df['Day'] = df.index.day
    df['Month'] = df.index.month

    high = STATION('ID', 'NOW', 0.0)
    low = STATION('ID', 'NOW', 500.0)
    grouped = df.groupby(by=['Day', 'Month'])
    for group in grouped:
        highs = group[1][
            group[1].Element == "TMAX"
        ].sort_values('Data_Value', ascending=False).head(1)

        lows = group[1][
            group[1].Element == "TMIN"
        ].sort_values('Data_Value', ascending=True).head(1)

        if (
            highs.index.year[0] == 2015 and
            (highs.Data_Value[highs.index[0]] / 10) > high.Value
        ):
            high = STATION(highs.ID[highs.index[0]], highs.index[0], highs.Data_Value[highs.index[0]] / 10)

        if (
            lows.index.year[0] == 2015 and
            (lows.Data_Value[lows.index[0]] / 10) < low.Value
        ):
            low = STATION(lows.ID[lows.index[0]], lows.index[0], lows.Data_Value[lows.index[0]] / 10)

    return high, low
