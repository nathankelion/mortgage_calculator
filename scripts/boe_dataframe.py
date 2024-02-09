import pandas as pd

def create_spot_curve():
    # Set the option to opt-in to the future behavior
    pd.set_option('future.no_silent_downcasting', True)

    # Load the Excel file
    excel_file_path = 'data\GLC Nominal daily data current month.xlsx'

    # Read the first sheet into a dataframe
    df_spot_short_end = pd.read_excel(excel_file_path, sheet_name='3. spot, short end')

    # Read the second sheet into another dataframe
    df_spot_curve = pd.read_excel(excel_file_path, sheet_name='4. spot curve')

    def clean_df_format(df, rows_to_remove, monthly_increment):    
        
        # Make a copy of the DataFrame
        df = df.copy()

        # Remove the first x rows
        df = df.iloc[rows_to_remove:]

        # Create column names
        column_names = ['date'] + [i * monthly_increment for i in range(1, len(df.columns))]

        # Assign column names
        df.columns = column_names

        # Convert 'date' column to datetime without time
        df['date'] = pd.to_datetime(df['date']).dt.date

        # Remove rows where all values (excluding 'date') are NaN
        df = df.dropna(subset=df.columns[1:], how='all')

        # Reset the index
        df = df.reset_index(drop=True)

        return df

    def coalesce_values(df):
        # Replace empty values with first available
        # Iterate over rows
        for index, row in df.iterrows():
            # Replace empty values in subsequent columns with the first non-empty value
            df.loc[index, df.columns[1:]] = df.loc[index, df.columns[1:]].ffill().bfill().infer_objects()

        return df

    # Run the dataframe cleaning functions
    df_spot_short_end = clean_df_format(df_spot_short_end, 3, 1)
    df_spot_curve = clean_df_format(df_spot_curve, 3, 6)
    df_spot_short_end = coalesce_values(df_spot_short_end)
    df_spot_curve = coalesce_values(df_spot_curve)

    # Create a new DataFrame with the first 5 years
    combined_df = df_spot_short_end.copy()

    # Column name
    new_column = df_spot_short_end.shape[1]
    new_columns = []

    while new_column <= 480:
        # Identify the nearest 6-month values for the current month
        if new_column % 6 in [1,2]:
            new_values = df_spot_curve[new_column - (new_column % 6)].values

        elif new_column % 6 in [3, 4, 5]:
            new_values = df_spot_curve[new_column + 6 - (new_column % 6)].values

        elif new_column % 6 == 0:
            new_values = df_spot_curve[new_column].values

        # Append the new column to the list
        new_columns.append(pd.Series(new_values, name=new_column))

        new_column += 1

    # Concatenate all the new columns to the combined_df
    combined_df = pd.concat([combined_df] + new_columns, axis=1)

    return combined_df