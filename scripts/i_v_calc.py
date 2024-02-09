import pandas as pd
from scripts.boe_dataframe import create_spot_curve

def calc_i_v(i_spread):
    
    # Get the dataframe
    spot_curve = create_spot_curve()

    # Get the last row of the dataframe
    latest_date = spot_curve.iloc[-1]

    # Extract the date from the last row
    date = latest_date['date']

    # Initialise lists to store data
    months = []
    i_values = []
    v_values = []

    # Iterate through each column (excluding the 'date' column)
    for col_name, value in latest_date.items():
        if col_name != 'date':
            # Calculate 'i' as the value plus 'i_spread'
            i = (value + i_spread)/100
            # Calculate 'v' as (1 + value) ^ -years
            v = (1 + i)**-(1/12 * int(col_name))  # Cast col_name to int for calculation

            # Append to the lists
            months.append(col_name)
            i_values.append(i)
            v_values.append(v)

    # Create i_v dataframe
    i_v_df = pd.DataFrame({'month': months, 'i': i_values, 'v': v_values})

    return date, i_v_df