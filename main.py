import streamlit as st
import pandas as pd
import numpy as np

from annotated_text import annotated_text

raw_data = pd.read_csv('all-companies-list.csv', dtype={'BSE Code': str})

def main():
    st.sidebar.subheader("Fund Stock Screener")
    with st.sidebar.form("stock_screen_info"):
        st.write("Stock Screen Info")
        no_of_stocks = st.number_input("No. of Stocks", value=21, min_value=1, max_value=100)
        min_investment = st.number_input("Min. Investment", value=28106, min_value=1, max_value=100000)
        max_portfolio_allocation = st.number_input("Maximum Portfolio Allocation for a single stock", value=10, min_value=1, max_value=100)
        universe = st.multiselect("Universe", ["Large Cap", "Mid Cap", "Small Cap"], default=["Small Cap"])

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("No. of Stocks", no_of_stocks, "universe", universe, "Min. Investment", min_investment)

    avg_investment_value = round(min_investment/no_of_stocks, 2)
    max_stock_price = round(max_portfolio_allocation*min_investment/100, 2)
    annotated_text(
        (str(avg_investment_value), "Average Investment Value"),
        (str(max_stock_price), "Maximum Stock Price")
    )

    # Stock Search Base Dataframe
    st.subheader("Stock Search")
    df = raw_data.iloc[:, [0, 1, 2, 3, 4]]

    ## Small-Cap Filter
    #small_cap = df[251:].count()
    small_cap = df[251:].rename(columns={
                'Current Price':'Price'}
                )
    nse_bse_small_cap = small_cap.dropna().count()
    
    bse_only_list = small_cap["NSE Code"].isnull()
    bse_only = small_cap[bse_only_list]
    nse_only_list = small_cap["BSE Code"].isnull()
    nse_only = small_cap[nse_only_list]

    st.write(small_cap)
    annotated_text(
        "❄️",
        (str(sum(bse_only_list) + sum(nse_only_list)), "Only NSE & Only BSE"),
        (str(nse_bse_small_cap[0]), "Both NSE & BSE"),
        "❄️",
        (str(sum(bse_only_list) + sum(nse_only_list) + nse_bse_small_cap[0]), "Sum"),
        "❄️",
        (str(small_cap.count()[3]), "All Small Cap")
    )

    base_df = (small_cap.Price >= max_stock_price)
    st.write("Base DF", small_cap[base_df], small_cap[base_df].count())

if __name__ == "__main__":
    main()