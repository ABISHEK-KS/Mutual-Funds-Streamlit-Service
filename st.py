import pandas as pd 
import streamlit as st 
import numpy as np 
import time 
import os 
from mftool import Mftool 
import streamlit.components.v1 as components


def convert_df(df):
    return df.to_csv().encode("utf-8")

tool = Mftool() 

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("externalcss.css")

def show_home(): 
    st.markdown("<h1 style='text-align: center; color: white;'>The Amateur-Made Mutual Funds Web Service</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white;'>Made By ABISHEK K S</h1>", unsafe_allow_html=True) 
    st.image('giphy.gif')
    st.warning('Read Terms Before Proceeding')
    st.markdown("<h1 style='text-align: center; color: white;'>Terms</h1>", unsafe_allow_html=True)
    st.write('By using this service, you acknowledge the following rules : ')
    conds = {
        "C1 ": "I acknowledge that the Information is provided by Association of Mutual Funds in India.",
        "C2 ": "As goes the saying, I solemnly agree to the age-old blabbering of Mutual Fund Investments being subject to market risks",
        "C3" : "I Acknowledge that I shall read all MF Scheme Related Documents Carefully", 
        "C4": "I am aware of the fact that the accuracy of data is only as correct as provided on AMF INDIA", 
        "C5" : "The API and Documentation is available publicly, and I shall not steal this code written by a student", 
        "C6" : "That I have thoroughly read through all Clauses above"
    }
    st.table(conds)
    st.markdown("<h1 style='text-align: center; color: white;'>Help</h1>", unsafe_allow_html=True)
    st.write("Please feel free to refer to the help section for further information")

def show_help(): 
    st.markdown("<h1 style='text-align: center; color: white;'>Help</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white;'>Basics of this Service</h1>", unsafe_allow_html=True)   
    st.write("""
    ### Help Section

    1. **Home:** This button will take you back to the main page of the application.

    2. **Fund Scheme Details:** Clicking this button will provide you with detailed information about various mutual fund schemes, including their objectives, asset allocation, historical performance, and fund manager details.

    3. **MF NAV History:** Use this button to access the historical Net Asset Value (NAV) data of mutual funds. You can view the NAV trends over different time periods to analyze the fund's performance.

    4. **Calculate Returns:** This feature allows you to calculate the returns on your mutual fund investments. You can input the initial investment amount, time period, and expected rate of return to estimate your investment growth.

    5. **NAV by Date:** View historical NAV data for mutual funds on specific dates. This feature allows you to track NAV fluctuations over time and analyze market trends.
    """)

def fund_scheme_details(): 
    st.markdown("<h1 style='text-align: center; color: white;'>Get Fund Details</h1>", unsafe_allow_html=True)   
    st.info(' ')
    st.image('section3.jpg')
    st.info(' ')
    st.markdown("<h1 style='text-align: center; color: white;'>Choose from a variety of available schemes</h1>", unsafe_allow_html=True)   
    st.warning('Warning - Scheme Number needed. If you are unaware of the Scheme Number, please refer to other sections for obtaining the scheme number')
    inps = st.text_input("Scheme number : ")
    res = ((tool.get_scheme_details(inps)))
    if res:
        st.balloons()
        inner = {"Fund House": res["fund_house"], "Scheme Type ": res["scheme_type"], 
                "Scheme Category": res["scheme_category"], "Scheme Code ": str(inps), 
                "Scheme Name": res["scheme_name"], "Scheme Dates": res["scheme_start_date"]["date"], 
                "Nav": res["scheme_start_date"]["nav"]}
        st.table(inner)
        st.warning(' ')
        st.markdown("<h1 style='text-align: center; color: white;'>Download Basics</h1>", unsafe_allow_html=True)
        df = pd.DataFrame(inner.items(), columns=["Labels", "Elucidations"])
        with st.spinner('Building Dataframe'):
            fname = str(inps) + '.csv'
        st.write("Download the above data as a csv file")
        d = st.download_button("Download Basic Data", data=convert_df(df), file_name=fname, mime="text/csv")

def mf_nav_history(): 
    st.markdown("<h1 style='text-align: center; color: white;'>MF NAV HISTORY</h1>", unsafe_allow_html=True)
    st.image("hist1.gif")
    st.markdown("<h3 style='text-align: center; color: white;'>History may repeat itself</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: white;'>That's why checking it out is important</h5>", unsafe_allow_html=True)
    st.info(' ')
    st.write("Enter Scheme Number to retrieve details")
    sear = st.text_input(label="Download MF Historicals")
    a = tool.get_scheme_historical_nav(sear, as_Dataframe=True)
    counter = 0
    fname = str(sear) + '.csv'
    if sear:
        with st.status('Fetching Details........'): 
            counter += 1
            st.write("Success")
            st.balloons()
            
        down = st.download_button(label="Download Now", file_name=fname, mime="csv", data=convert_df(a))
        st.balloons()
        st.info(' ')
        st.markdown("<h5 style='text-align: center; color: white;'>Important info</h5>", unsafe_allow_html=True)
        st.title("Precautionary Warning for Mutual Fund Price Data Analysis")

        st.write("""
        Caution: When analyzing mutual fund price data, it's essential to approach it with caution and diligence. Here are some precautions to keep in mind:

        1. **Understand Fund Characteristics**: Mutual funds can vary widely in their objectives, strategies, and risk profiles. Ensure you understand the specific characteristics of the fund you're analyzing.

        2. **Verify Data Accuracy**: While the provided data appears accurate, always verify its reliability. Check for any potential errors or discrepancies in the dataset before making investment decisions.

        3. **Consider Fund Performance**: Evaluate the fund's performance over different time periods to assess its consistency and long-term potential. Remember that past performance is not indicative of future results.

        4. **Assess Fees and Expenses**: Mutual funds typically charge fees and expenses that can impact overall returns. Understand the fee structure and consider the impact on your investment over time.

        5. **Diversification**: Consider diversifying your investment portfolio across different asset classes and funds to mitigate risk. Avoid placing undue reliance on a single mutual fund.

        6. **Consult a Financial Advisor**: If you're unsure about interpreting the data or making investment decisions, seek advice from a qualified financial advisor. They can provide personalized guidance based on your financial goals and risk tolerance.

        Remember, investing in mutual funds involves risks, and careful analysis and consideration of various factors are essential for making informed investment decisions.
        """)   
            
def calc_return(): 
    st.info(' ')
    st.markdown("<h1 style='text-align: center; color: white;'>Calculate Current Value</h1>", unsafe_allow_html=True)
    st.image('rising-going-up.gif')
    st.info('  ')
    st.markdown("<h3 style='text-align: center; color: white;'>Compute Market Value here</h3>", unsafe_allow_html=True)
    st.write("Please provide us with the number of units you have")
    inps = st.text_input(label="Enter the no: of units here ")
    scheme = st.text_input(label="Enter Scheme Number here")
    if inps and scheme:
        with st.status("Calculating"): 
            st.balloons()
        result = tool.calculate_balance_units_value(scheme, inps)
        if result:
            st.table(result)
        else:
            st.warning("Invalid Scheme Number or Units. Please check your input.")

def nav_by_date():
    st.markdown("<h1 style='text-align: center; color: white;'>NAV by Date</h1>", unsafe_allow_html=True)
    st.image("calendar-months.gif")
    st.info(' ')
    st.markdown("<h3 style='text-align: center; color: white;'>DATES ARE IMPORTANT :) </h3>", unsafe_allow_html=True)

    st.write("Enter Scheme Number to retrieve NAV details")
    scheme = st.text_input(label="Enter Scheme Number here")
    
    if scheme:
        sdate = st.text_input(label="Enter Starting Date (DD-MM-YYYY)")
        if sdate:
            ldate = st.text_input(label="Enter Ending Date (DD-MM-YYYY)")
            if ldate:
                with st.spinner('Retrieving...'):
                    try:
                        response = tool.get_scheme_historical_nav_for_dates(scheme, sdate, ldate)
                        if 'data' in response:
                            nav_data = response['data']
                            if nav_data:
                                df = pd.DataFrame(nav_data)
                                st.balloons()
                                with st.status('Generating CSV...'):
                                    st.write("Download the above data as a csv file")
                                    fname = f"{scheme}_{sdate}_to_{ldate}.csv"
                                    st.download_button("Download NAV Data", data=convert_df(df), file_name=fname, mime="text/csv")
                            else:
                                st.warning("No NAV data available for the selected date range")
                        else:
                            st.warning("No data found in the response")
                    except Exception as e:
                        st.error(f"Error retrieving data: {e}")
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Home"

Home = st.sidebar.button('Home')
hand = st.sidebar.button('Help & Docs')
fsdet = st.sidebar.button('Fund Scheme Details')
navhist = st.sidebar.button('MF NAV History')
calc_returns = st.sidebar.button('Calculate Current Value')
navbydate = st.sidebar.button('NAV by Date')

if Home:
    st.session_state.selected_page = "Home"
if hand: 
    st.session_state.selected_page = "hand"   
if fsdet:
    st.session_state.selected_page = "Fund Scheme Details"
if navhist:
    st.session_state.selected_page = "MF NAV History"
if calc_returns:
    st.session_state.selected_page = "Calculate Current Value"
if navbydate:
    st.session_state.selected_page = "NAV by Date"

if st.session_state.selected_page == "Home":
    show_home() 
elif st.session_state.selected_page == "hand": 
    show_help()   
elif st.session_state.selected_page == "Fund Scheme Details": 
    fund_scheme_details()
elif st.session_state.selected_page == "MF NAV History": 
    mf_nav_history()  
elif st.session_state.selected_page == "Calculate Current Value": 
    calc_return()
elif st.session_state.selected_page == "NAV by Date": 
    nav_by_date()
