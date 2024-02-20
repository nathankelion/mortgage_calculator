# Calculates stamp duty
def calculate_stamp_duty(house_price, first_time_buyer):
    stamp_duty = 0
    if house_price > 1500000:
        stamp_duty += ((house_price - 1500000) * 0.12)
        stamp_duty += (575000 * 0.1)
        stamp_duty += (675000 * 0.05)
    
    elif house_price > 925000:
        stamp_duty += ((house_price - 925000) * 0.1)
        stamp_duty += (675000 * 0.05)

    elif (house_price > 250000 and first_time_buyer == False) or house_price > 625000:
        stamp_duty += ((house_price - 250000) * 0.05)

    elif house_price <= 625000 and house_price > 250000 and first_time_buyer == True:
        stamp_duty += ((house_price - 425000) * 0.05)
    
    return stamp_duty

# Calculates average interest
def calculate_average_i(i_v_df, pv_list, mortgage_term, borrowed):
    total_sum = 0
    for value, row in i_v_df.iterrows():
        if row['month'] <= mortgage_term*12:
            total_sum += (row['i'] * pv_list[value])
    average_i = (total_sum/borrowed)*100
    return average_i