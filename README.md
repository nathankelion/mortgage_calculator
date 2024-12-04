# Mortgage Calculator Web Application

## Overview

This web application provides two key mortgage calculators:

1. **Monthly Mortgage Calculator** – Calculates the monthly repayment for a mortgage based on the loan amount, interest rate, and repayment term.
2. **Affordability Calculator** – Estimates the maximum affordable house price based on desired monthly repayments, taking into account factors such as first-time buyer status and Stamp Duty implications.

The application is built using **Python** and **Streamlit**, providing an interactive and user-friendly interface for users to make informed decisions about mortgages.

Additionally, the system is automated to ensure real-time accuracy by updating the Bank of England base rate daily using **GitHub Actions**, incorporating the latest interest rate data into the calculations.

## Features

- **Monthly Mortgage Calculator**: 
  - Calculates monthly repayments.
  - Inputs: Loan amount, interest rate, repayment term.
  - Output: Monthly repayment amount.

- **Affordability Calculator**: 
  - Estimates the maximum affordable house price based on the user's desired monthly repayments.
  - Takes into account first-time buyer status and Stamp Duty implications.
  - Output: Maximum affordable house price.

- **Automated Daily Updates**: 
  - The system automatically updates the Bank of England base rate every day using **GitHub Actions**.
  - Ensures real-time mortgage calculations based on the latest interest rates.

## Technologies Used

- **Python**: The primary programming language used for calculations and automation.
- **Streamlit**: A Python library for building interactive web applications.
- **Scipy**: Used for complex mathematical calculations related to mortgage formulas.
- **GitHub Actions**: Automates daily data updates from the Bank of England.
- **Requests**: Used for downloading data from online sources.

## Installation

To run the Mortgage Calculator Web Application locally, follow these steps:

### Prerequisites

- **Python** (version 3.7 or higher)
- **pip** (Python package manager)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/mortgage-calculator.git
   cd mortgage-calculator
   
2. **Create and activate a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use venv\Scripts\activate

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Run the Streamlit app**:
   ```bash
   streamlit run app.py

The application will open in your default web browser at http://localhost:8501.

## Automated Updates with GitHub Actions
This project utilizes GitHub Actions to automatically update the Bank of England base rate each day and ensure real-time accuracy for the calculations.

To trigger the scheduled updates manually or view the status of the update jobs, visit the Actions tab in the GitHub repository.

## Contributing
Feel free to fork this project and make contributions. If you encounter any issues or have ideas for improvement, please open an issue or submit a pull request.

### Steps to contribute:
1. Fork the repository
2. Clone the forked repository
3. Create a new branch: git checkout -b feature-branch
4. Make your changes
5. Commit your changes: git commit -m "Add feature"
6. Push to your branch: git push origin feature-branch
7. Create a pull request