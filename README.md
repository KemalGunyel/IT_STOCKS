# Interactive EDA for Tech Stocks

This Streamlit application provides an interactive exploratory data analysis (EDA) for technology stocks. The app allows users to select multiple tech stocks, view their closing prices, trading volumes, moving averages, and various other analyses. 

## Features

- Select multiple tech stocks for analysis
- View closing prices over time
- View trading volumes over time
- View 30-day and 90-day moving averages
- View correlation matrix of daily returns
- Optional plots for rolling volatility and volume vs. closing price
- Display descriptive statistics for the selected stocks


## Data

The application uses a CSV file named `combined_tech_stocks_data.csv` which should be placed in the same directory as the `app.py` file. This file should contain the stock data with at least the following columns:
- `Date`
- `Symbol`
- `Close`
- `Volume`

## Usage

1. **Load the data**: The application reads the stock data from `combined_tech_stocks_data.csv` and performs necessary calculations such as daily returns and moving averages.

2. **Select stocks**: Use the sidebar to select up to three tech stocks for analysis.

3. **Set date range**: Use the date picker in the sidebar to select the date range for the analysis.

4. **View plots**: The application displays various plots including closing prices, trading volumes, moving averages, and correlation matrices.

5. **Optional plots**: Enable additional plots for rolling volatility and volume vs. closing price using the checkboxes in the sidebar.

6. **Descriptive statistics**: View the descriptive statistics for the selected stocks.



