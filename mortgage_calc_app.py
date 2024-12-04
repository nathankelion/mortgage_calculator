import streamlit as st
import base64
from scipy.optimize import root_scalar

from scripts.boe_dataframe import create_spot_curve
from scripts.i_v_calc import calc_i_v
from scripts.output_calculations import calculate_stamp_duty, calculate_average_i

# Set page configuration
st.set_page_config(page_title='JNK Mortgage Calculator', page_icon=':house:', layout="wide")


# Columns for format
col1, col2 = st.columns([12,1])

# Add an image of a house
col2.image('data/house.webp')

# Display title
col1.title('Mortgage Calculator')

@st.cache_data
def get_yield_date():
    yield_date = create_spot_curve()[0]
    return yield_date
# Get the date of the latest yields
yield_date = get_yield_date()

# Brief explanation
st.write(f'Bank of England spot rates as at *{yield_date.strftime("%d/%m/%Y")}*')

st.divider()

# Columns for format
col1, col2, col3, col4 = st.columns([4,2,4,2])

# Determine whether Monthly Mortgage Calculator or Affordability Calculator
calculator_type = col1.selectbox("Select calculator",["Monthly mortgage calculator", "Affordability calculator"], help="Choose between calculators:\n\n\'Monthly mortgage calculator' works out monthly repayments based on borrowing.\n\n'Affordablity calculator' works out  theoretical maximum house price based on desired monthly repayments.")

# Option calculator dependent
if calculator_type == "Monthly mortgage calculator":
    # House Price
    house_price = col1.number_input('Enter house price (£)', step=50000, min_value=0, value=0, format="%d")

elif calculator_type == "Affordability calculator":
    # Monthly Payment
    monthly_payment = col1.number_input('Enter desired monthly repayment (£)', step=250, min_value=0, value=0, format="%d")

# Deposit
# Radio button to choose between % and £
if calculator_type == 'Monthly mortgage calculator':
    deposit_type = col1.radio("Select deposit type:", ["£", "%"])

    if deposit_type == "£":
        # Add deposit box
        deposit_money = col1.number_input("Enter deposit (£)", min_value=0, value=0, step=5000,format="%d", help='Typically 10% of the house price. Consider stampt duty when determining deposit.')

    elif deposit_type == "%":
        # Add deposit box
        deposit_percentage = col1.number_input("Enter deposit (%)", min_value=0.00, max_value=100.00, value=0.00, step=5.00, help='Typically 10% of the house price. Consider stamp duty when determining deposit.')

elif calculator_type == 'Affordability calculator':
    # Add deposit box
    deposit = col1.number_input("Enter deposit (£)", min_value=0, value=0, step=5000,format="%d", help='Typically 10% of the house price. Consider stamp duty when determing deposit.')

# Checkbox for first time buyer
first_time_buyer = col1.checkbox("Tick if you're a first time buyer", help="This may affect stamp duty")

# Mortgage term
mortgage_term = col1.slider("Mortgage term (years)", min_value=5, max_value=30, value=20, step=1)

# Advanced options (i spread)
advanced_options = col1.toggle("Advanced options")

i_spread_default = 0.75

if advanced_options:
    i_spread = col1.number_input("Interest rate spread (% pa)", min_value=0.00, max_value=5.00, value=i_spread_default, step=0.05, help="Typically 0.5-1.5% pa, depentant on financial conditions")

else:
    i_spread = i_spread_default

# Columns for format
buff, col4, buff = col1.columns([1,2,1])

# Calculate button
calculate_clicked = col4.button("Calculate", use_container_width=True)

@st.cache_data
def get_i_v_df(i_spread):
    i_v_df = calc_i_v(i_spread)
    return i_v_df

if calculate_clicked:
    # Load the dataframe
    i_v_df = get_i_v_df(i_spread)

    # Monthly Mortgage Calculation
    if calculator_type == 'Monthly mortgage calculator':
        # Make sure deposit is in money
        if deposit_type =="£":
            deposit = deposit_money
        elif deposit_type=="%":
            # If deposit is in percentage, calculate the actual deposit amount based on the house price
            deposit = house_price*(deposit_percentage/100)
            
        if house_price == 0 or deposit >= house_price:
            # Display an error message if the house price is not a positive value
            col3.error('Please ensure you provide a house price and that this price is larger than your deposit')
        else:
            # Define the objective function
            def objective_function(monthly_payment):
                borrowed = house_price - deposit
                pv_list = [(v * monthly_payment) for v in i_v_df['v']]
                return borrowed - sum(pv_list[:(mortgage_term*12)])

            # Set initial guesses for the monthly payment
            initial_guess_lower = 0
            initial_guess_upper = 1000000

            # Use root_scalar to find the monthly payment that satisfies the objective function
            result = root_scalar(objective_function, bracket=[initial_guess_lower, initial_guess_upper], method='bisect')

            # The result object contains the solution
            monthly_payment_solution = result.root

            # Calculate average interest
            borrowed = house_price - deposit
            pv_list = [(v * monthly_payment_solution) for v in i_v_df['v']]
            
            average_i = calculate_average_i(i_v_df, pv_list, mortgage_term, borrowed)

            # Calculate the total payments over the mortgage term
            total_repayments = monthly_payment_solution * (mortgage_term*12)


            # Calculate stamp duty
            stamp_duty = calculate_stamp_duty(house_price, first_time_buyer)

            # Format numbers to include commas
            monthly_payment_solution, average_i, total_repayments, stamp_duty = format(round(monthly_payment_solution), ',d'), round(average_i,2), format(round(total_repayments), ',d'), format(round(stamp_duty), ',d')
            
            # Print user inputs
            if deposit_type == '£':
                col3.write(f"<span style='font-size: small; font-style: italic;'>Based on a house price of £{format(house_price, ',d')}, initial deposit of £{format(deposit_money, ',d')}, and an interest rate spread of {round(i_spread, 2)}% pa</span>", unsafe_allow_html=True)
            
            elif deposit_type == '%':
                col3.write(f"<span style='font-size: small; font-style: italic;'>Based on a house price of £{format(house_price, ',d')}, initial deposit of {round(deposit_percentage,2)}%, and an interest rate spread of {round(i_spread,2)}% pa</span>", unsafe_allow_html=True)

            # Display the success box with calculated results
            col3.success(
                "Monthly payment: £{0}\n\nAverage interest: {1}% pa\n\nTotal rerepayments: £{2}\n\nStamp Duty: {3}".format(
                    monthly_payment_solution, average_i, total_repayments, stamp_duty
                )
            )


    # Affordaility Calculation
    if calculator_type == 'Affordability calculator':
        if monthly_payment == 0:
            # Display an error message if the monthly payment is not a positive value
            col3.error('Must enter a positive value for monthly payment')
        else:
            # Calculate adjusted payments
            pv_list = [(v * monthly_payment) for v in i_v_df['v']]
            
            # Calculate the maximum house price including the deposit
            max_borrow = sum(pv_list[:(mortgage_term*12)])
            house_price = max_borrow + deposit

            # Calculate average interest
            average_i = calculate_average_i(i_v_df, pv_list, mortgage_term, max_borrow)

            # Calculate the total payments over the mortgage term
            total_repayments = monthly_payment * (mortgage_term*12)

            # Calculate stamp duty
            stamp_duty = calculate_stamp_duty(house_price, first_time_buyer)

            # Format numbers to include commas
            house_price, average_i, total_repayments, stamp_duty = format(round(house_price), ',d'), round(average_i,2), format(round(total_repayments), ',d'), format(round(stamp_duty), ',d')

            # Print their inputs
            col3.write(f"<span style='font-size: small; font-style: italic;'>Based on a monthly repayment of £{format(monthly_payment, ',d')}, initial deposit of £{format(deposit, ',d')}, and an interest rate spread of {round(i_spread,2)}% pa</span>", unsafe_allow_html=True)

            # Display the success box with calculated results
            col3.success(
                "Maximum house price: £{0}\n\nAverage interest: {1}% pa\n\nTotal repayments: £{2}\n\nStamp Duty: {3}".format(
                    house_price, average_i, total_repayments, stamp_duty
                )
            )


    # File path to the image
image_path = "data/mortgage_info_website.png"

# Website URL to link to
website_url = "https://www.moneysavingexpert.com/mortgages/best-mortgages-cashback/"

try:
    # Encode the image as base64
    with open(image_path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode()

    # Define HTML and CSS for the tooltip and clickable image
    html_content_house = f"""
    <style>
    .tooltip-container {{
        position: relative;
        display: inline-block;
        cursor: pointer;
    }}

    .tooltip-container img {{
        width: 300px; /* Adjust the size of the image as needed */
        border-radius: 10px; /* Optional: Rounded corners */
        transition: transform 0.2s; /* Smooth hover effect */
    }}

    .tooltip-container img:hover {{
        transform: scale(1.05); /* Slight zoom on hover */
    }}

    .tooltip {{
        visibility: hidden;
        width: 220px;
        background-color: black;
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        top: 100%; /* Position below the image */
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
    }}

    .tooltip-container:hover .tooltip {{
        visibility: visible;
        opacity: 1;
    }}
    </style>

    <div class="tooltip-container">
        <a href="{website_url}" target="_blank">
            <img src="data:image/png;base64,{img_data}" alt="Mortgage Info">
        </a>
        <div class="tooltip">Click to visit the website</div>
    </div>
    """

    # Display HTML in Streamlit
    col3.markdown(html_content_house, unsafe_allow_html=True)

except FileNotFoundError:
    st.error(f"File not found: {image_path}. Please check the file path and try again.")

# Read the GitHub logo image file and encode it
with open("data/GitHub_Invertocat_Logo.svg", "rb") as github_img_file:
    github_img_data = base64.b64encode(github_img_file.read()).decode()

# Define the URLs
github_url = "https://github.com/nathankelion/mortgage_calculator"



# Define HTML and CSS for the logos container
html_content_logos = f"""
<style>
.logos-container {{
    position: fixed;
    bottom: 10px;
    right: 10px;
    display: flex;
    flex-direction: row-reverse;
    justify-content: flex-end;
    align-items: center;
    gap: 5px;
    z-index: 1000; /* Ensure it appears above other content */
}}
.logo {{
    cursor: pointer;
    width: auto;
    height: 30px;
}}
.logo img {{
    width: 30px;
    height: auto;
}}
.tooltip {{
    visibility: hidden;
    width: fit-content;
    background-color: black;
    color: white;
    text-align: center;
    border-radius: 6px;
    padding: 4px;
    position: absolute;
    z-index: 1001;
    bottom: 40px; /* Adjust to be above the logo */
    left: 50%;
    transform: translateX(-50%);
    font-size: smaller;
}}
.logo:hover .tooltip {{
    visibility: visible;
}}
</style>

<div class="logos-container">
    <div class="logo">
        <a href="{github_url}" target="_blank">
            <img src="data:image/svg+xml;base64,{github_img_data}" alt="GitHub Logo">
        </a>
        <span class="tooltip">Visit GitHub Repo</span>
    </div>
</div>
"""

# Display HTML in Streamlit
st.markdown(html_content_logos, unsafe_allow_html=True)

# Add a line with your information, fixed at the bottom center
st.markdown(
    """<div style='position: fixed; bottom: 10px; width: 100%; text-align: center;'><i>A JNK Product 2024</i></div>""",
    unsafe_allow_html=True
)


# Add a line with your information, using CSS to position it at the bottom
st.markdown(
    """<div style='position: fixed; bottom: 10px; width: 100%; text-align: center;'><i>A JNK Product 2024</i></div>""",
    unsafe_allow_html=True
)