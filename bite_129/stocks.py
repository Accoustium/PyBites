import requests

STOCK_DATA = 'https://bit.ly/2MzKAQg'

# pre-work: load JSON data into program

with requests.Session() as s:
    data = s.get(STOCK_DATA).json()


# your turn:

def _cap_str_to_mln_float(cap):
    """If cap = 'n/a' return 0, else:
       - strip off leading '$',
       - if 'M' in cap value, strip it off and return value as float,
       - if 'B', strip it off and multiple by 1,000 and return
         value as float"""
    if cap == "n/a":
        return 0
    elif "m" in cap.lower():
        return float(cap.strip("$")[:-1])
    elif "b" in cap.lower():
        return float(cap.strip("$")[:-1]) * 1000


def get_industry_cap(industry):
    """Return the sum of all cap values for given industry, use
       the _cap_str_to_mln_float to parse the cap values,
       return a float with 2 digit precision"""
    cap = 0
    for id in data:
        if id['industry'] == industry:
            cap += _cap_str_to_mln_float(id['cap'])

    return float("{0:.2f}".format(cap))


def get_stock_symbol_with_highest_cap():
    """Return the stock symbol (e.g. PACD) with the highest cap, use
       the _cap_str_to_mln_float to parse the cap values"""
    high_sym = ""
    high_cap = 0
    for id in data:
        if _cap_str_to_mln_float(id['cap']) > high_cap:
            high_cap = float("{0:.2f}".format(
                _cap_str_to_mln_float(id['cap'])
            ))
            high_sym = id['symbol']

    return high_sym


def get_sectors_with_max_and_min_stocks():
    """Return a tuple of the sectors with most and least stocks,
       discard n/a"""
    from collections import Counter
    sector = Counter()
    for id in data:
        sector[id['sector']] += 1

    sector.pop("n/a")

    return (sector.most_common()[0][0], sector.most_common()[-1][0])
