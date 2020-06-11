import pandas as pd

data = "https://s3.us-east-2.amazonaws.com/bites-data/menu.csv"
# load the data in once, functions will use this module object
df = pd.read_csv(data)

pd.options.mode.chained_assignment = None  # ignore warnings


def get_food_most_calories(df=df):
    """Return the food "Item" string with most calories"""
    return df.sort_values('Calories', ascending=False).head(1).Item.values[0]


def get_bodybuilder_friendly_foods(df=df, excl_drinks=False):
    """Calulate the Protein/Calories ratio of foods and return the
       5 foods with the best ratio.

       This function has a excl_drinks switch which, when turned on,
       should exclude 'Coffee & Tea' and 'Beverages' from this top 5.

       You will probably need to filter out foods with 0 calories to get the
       right results.

       Return a list of the top 5 foot Item stings."""
    df['ratio'] = df.Protein / df.Calories
    if not excl_drinks:
        return list(df[(df.Calories != 0)].sort_values('ratio', ascending=False).head(5).Item.values)
    else:
        new_df = df.loc[(df.Category != 'Coffee & Tea') & (df.Category != 'Beverages')]
        return list(new_df[(new_df.Calories != 0)].sort_values('ratio', ascending=False).head(5).Item.values)