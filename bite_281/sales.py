import json
import os
from pathlib import Path
from typing import Dict, List, Union

import pandas as pd  # type: ignore
import requests

URL: str = "https://bites-data.s3.us-east-2.amazonaws.com/MonthlySales.csv"
STATS: List[str] = ["sum", "mean", "max"]
TMP: Path = Path(os.getenv("TMP", "/tmp")) / "MonthlySales.csv"


def get_data(url: str) -> Dict[str, str]:
    """Get data from Github

    Args:
        url (str): The URL where the data is located.

    Returns:
        Dict[str, str]: The dictionary extracted from the data
    """
    if TMP.exists():
        data = json.loads(TMP.read_text())
    else:
        response = requests.get(url)
        response.raise_for_status()
        data = json.loads(response.text)
        with TMP.open("w") as tmp:
            json.dump(data, tmp)
    return data


def process_data(url: str) -> pd.DataFrame:
    """Process the data from the Github API

    Args:
        url (str): The URL where the data is located.

    Returns:
        pd.DataFrame: Pandas DataFrame generated from the processed data
    """
    import base64
    data = get_data(url)

    decoded_string = base64.b64decode(data['content'])
    frame = pd.DataFrame(
        [row.split(',') for row in str(decoded_string, 'utf-8').split('\r\n')]
    )

    header = frame.iloc[0]
    frame = frame[1:]
    frame.rename(columns=header, inplace=True)
    frame.month = pd.DatetimeIndex(frame.month)
    frame.sales = frame.sales.astype('float')

    return frame


def summary_report(df: pd.DataFrame, stats: Union[List[str], None] = STATS) -> None:
    """Summary report generated from the DataFrame and list of stats

    Will aggregate statistics for sum, mean, and max by default.

    Args:
        df (pd.DataFrame): Pandas DataFrame of the Github API data
        stats (List[str], optional): List of summaries to aggregate. Defaults to STATS.

    Returns:
        None (prints to standard output)

        Example:
                    sum          mean        max
        year
        2013  484247.51  40353.959167   81777.35
        2014  470532.51  39211.042500   75972.56
        2015  608473.83  50706.152500   97237.42
        2016  733947.03  61162.252500  118447.83
    """
    new_df = df.copy()
    new_df.set_index(new_df.month, inplace=True)
    new_df.drop(columns=['month'], inplace=True)
    summary = new_df.groupby(new_df.index.year)

    new_summary = pd.DataFrame([])
    for stat in stats:
        frame = eval(f"summary.{stat}()")
        frame.columns = [stat]
        if new_summary.empty is True:
            new_summary = frame.copy()
        else:
            new_summary = new_summary.join(frame.copy())

    new_summary.index.name = 'year'

    print(new_summary)


def yearly_report(df: pd.DataFrame, year: int) -> None:
    """Generate a sales report for the given year

    Args:
        df (pd.DataFrame): Pandas DataFrame of the Github API data
        year (int): The year to generate the report for

    Raises:
        ValueError: Error raised if the year requested is not in the data.
        Should be in the form of "The year YEAR is not included in the report!"

    Returns:
        None (prints to standard output)

        Example:
        2013
                  sales
        month
        1      14236.90
        2       4519.89
        3      55691.01
        4      28295.35
        5      23648.29
        6      34595.13
        7      33946.39
        8      27909.47
        9      81777.35
        10     31453.39
        11     78628.72
        12     69545.62
    """
    new_df = df.copy()
    new_df.set_index('month', inplace=True)
    yearly = new_df[new_df.index.year == year]

    if yearly.empty is True:
        raise ValueError(f"The year {year} is not included in the report!")

    print("\n".join(["", str(year), str(yearly.groupby([yearly.index.month]).sum().copy())]))


# uncomment the following for viewing/testing the reports/code
# if __name__ == "__main__":
#     data = process_data(URL)
#     summary_report(data)
#     for year in (data["month"].dt.year).unique():
#         yearly_report(data, year)
#
#     yearly_report(data, 2020)