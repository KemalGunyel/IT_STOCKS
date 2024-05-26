import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
combined_df = pd.read_csv('combined_tech_stocks_data.csv')
combined_df['Date'] = pd.to_datetime(combined_df['Date'])

# Calculate daily returns
combined_df['Daily Return'] = combined_df.groupby('Symbol')['Close'].pct_change()

# Calculate moving averages: 30 days and 90 days
for symbol in combined_df['Symbol'].unique():
    combined_df.loc[combined_df['Symbol'] == symbol, 'MA30'] = combined_df[combined_df['Symbol'] == symbol]['Close'].rolling(window=30).mean()
    combined_df.loc[combined_df['Symbol'] == symbol, 'MA90'] = combined_df[combined_df['Symbol'] == symbol]['Close'].rolling(window=90).mean()

# Volatility Analysis: Calculate rolling standard deviation of daily returns
combined_df['Volatility'] = combined_df.groupby('Symbol')['Daily Return'].rolling(window=30).std().reset_index(0, drop=True)

# Streamlit app layout
st.title("Interactive EDA for Tech Stocks")

# Sidebar for symbol selection
st.sidebar.header("Stock Selection")
symbols = combined_df['Symbol'].unique()
symbol1 = st.sidebar.selectbox("Select First Symbol", symbols, index=0)
symbol2 = st.sidebar.selectbox("Select Second Symbol", symbols, index=1)
symbol3 = st.sidebar.selectbox("Select Third Symbol", symbols, index=2)

# Date range input using st.date_input in the sidebar
min_date = combined_df['Date'].min()
max_date = combined_df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter data based on selections
start_date, end_date = date_range
filtered_df1 = combined_df[(combined_df['Symbol'] == symbol1) & 
                           (combined_df['Date'] >= pd.to_datetime(start_date)) & 
                           (combined_df['Date'] <= pd.to_datetime(end_date))]

filtered_df2 = combined_df[(combined_df['Symbol'] == symbol2) & 
                           (combined_df['Date'] >= pd.to_datetime(start_date)) & 
                           (combined_df['Date'] <= pd.to_datetime(end_date))]

filtered_df3 = combined_df[(combined_df['Symbol'] == symbol3) & 
                           (combined_df['Date'] >= pd.to_datetime(start_date)) & 
                           (combined_df['Date'] <= pd.to_datetime(end_date))]

# Create combined plot for closing prices
fig = go.Figure()

fig.add_trace(go.Scatter(x=filtered_df1['Date'], y=filtered_df1['Close'], mode='lines', name=f'{symbol1} Closing Prices'))
fig.add_trace(go.Scatter(x=filtered_df2['Date'], y=filtered_df2['Close'], mode='lines', name=f'{symbol2} Closing Prices'))
fig.add_trace(go.Scatter(x=filtered_df3['Date'], y=filtered_df3['Close'], mode='lines', name=f'{symbol3} Closing Prices'))

fig.update_layout(title='Closing Prices Over Time', xaxis_title='Date', yaxis_title='Close Price')
st.plotly_chart(fig)

# Create combined plot for volumes
fig_volume = go.Figure()

fig_volume.add_trace(go.Bar(x=filtered_df1['Date'], y=filtered_df1['Volume'], name=f'{symbol1} Volume'))
fig_volume.add_trace(go.Bar(x=filtered_df2['Date'], y=filtered_df2['Volume'], name=f'{symbol2} Volume'))
fig_volume.add_trace(go.Bar(x=filtered_df3['Date'], y=filtered_df3['Volume'], name=f'{symbol3} Volume'))

fig_volume.update_layout(title='Trading Volume Over Time', xaxis_title='Date', yaxis_title='Volume', barmode='group')
st.plotly_chart(fig_volume)



# Correlation Matrix of Daily Returns
st.header("Correlation Matrix of Daily Returns")
correlation_matrix = combined_df.pivot_table(values='Daily Return', index='Date', columns='Symbol').corr()
fig_corr = px.imshow(correlation_matrix, text_auto=True, title='Correlation Matrix of Daily Returns', labels=dict(color="Correlation"))
st.plotly_chart(fig_corr)

# Create combined plot for 30-day moving averages
fig_ma30 = go.Figure()

fig_ma30.add_trace(go.Scatter(x=filtered_df1['Date'], y=filtered_df1['MA30'], mode='lines', name=f'{symbol1} 30-day MA'))
fig_ma30.add_trace(go.Scatter(x=filtered_df2['Date'], y=filtered_df2['MA30'], mode='lines', name=f'{symbol2} 30-day MA'))
fig_ma30.add_trace(go.Scatter(x=filtered_df3['Date'], y=filtered_df3['MA30'], mode='lines', name=f'{symbol3} 30-day MA'))

fig_ma30.update_layout(title='30-day Moving Average Over Time', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig_ma30)

# Create combined plot for 90-day moving averages
fig_ma90 = go.Figure()

fig_ma90.add_trace(go.Scatter(x=filtered_df1['Date'], y=filtered_df1['MA90'], mode='lines', name=f'{symbol1} 90-day MA'))
fig_ma90.add_trace(go.Scatter(x=filtered_df2['Date'], y=filtered_df2['MA90'], mode='lines', name=f'{symbol2} 90-day MA'))
fig_ma90.add_trace(go.Scatter(x=filtered_df3['Date'], y=filtered_df3['MA90'], mode='lines', name=f'{symbol3} 90-day MA'))

fig_ma90.update_layout(title='90-day Moving Average Over Time', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig_ma90)

# Optional plots
show_volatility = st.sidebar.checkbox("Show Volatility Plot")
show_scatter = st.sidebar.checkbox("Show Volume vs. Closing Price Plot")

if show_volatility:
    # Sidebar for selecting symbols for the volatility plot
    selected_symbols_volatility = st.sidebar.multiselect("Select Symbols for Volatility Plot", symbols)

    # Filter data based on selected symbols
    filtered_volatility_df = combined_df[combined_df['Symbol'].isin(selected_symbols_volatility)]

    # Create plot for volatility
    fig_volatility = px.line(filtered_volatility_df, x='Date', y='Volatility', color='Symbol', 
                             title='30-Day Rolling Volatility of Tech Stocks')
    st.plotly_chart(fig_volatility)

if show_scatter:
    # Sidebar for selecting symbols for the scatter plot
    selected_symbols_scatter = st.sidebar.multiselect("Select Symbols for Volume vs. Closing Price Plot", symbols)

    # Filter data based on selected symbols
    filtered_scatter_df = combined_df[combined_df['Symbol'].isin(selected_symbols_scatter)]

    # Scatter plot of Volume vs. Closing Price
    fig_scatter = px.scatter(filtered_scatter_df, x='Close', y='Volume', color='Symbol', 
                             title='Volume vs. Closing Price of Stocks')
    fig_scatter.update_layout(xaxis_title='Close Price', yaxis_title='Volume')
    st.plotly_chart(fig_scatter)


# Display descriptive statistics for all three stocks
st.header("Descriptive Statistics")
st.subheader(f'{symbol1} Statistics')
st.write(filtered_df1.describe())

st.subheader(f'{symbol2} Statistics')
st.write(filtered_df2.describe())

st.subheader(f'{symbol3} Statistics')
st.write(filtered_df3.describe())









