import streamlit as st
import pandas as pd

import utils as u

import src.home
# import src.statistics


st.set_page_config(
		page_title="Operations at PAE and MWH airports",
		page_icon="🛩️",
		layout="wide",
		initial_sidebar_state="expanded",
	)

PAGES = {
	"Home": src.home, 
	# "Descriptive statistics": src.statistics, 
}

#####

def main():
	data = get_data()
	
	# application architecture
	st.sidebar.title("Operations at PAE and MWH Airports 🛩️🌎")
	st.sidebar.subheader("Navigation")
	selection = st.sidebar.radio("Go to", list(PAGES.keys()))

	page = PAGES[selection]

	with st.spinner(f"Loading {selection} ..."):
		page.write(data)

	st.sidebar.info("**Author:** Steffen Coenen")
	
	st.sidebar.info("**Full material:** The complete dataset and all code is available at the corresponding [GitHub repository](https://github.com/steffen-coe/Airport-Operations).")

@st.cache(allow_output_mutation=True)
def get_data():
	# df = pd.read_csv("data/ATADS Airport Operations Report (SEA, PAE, MWH)_fix_cleaned.csv", header=7)
	df = pd.read_excel("data/WEB-Report-90921.xlsx", header=7, skipfooter=5)
	df_key = pd.read_csv("data/key.csv", index_col="column_name")
	df.columns = df_key.index
	
	df.columns = [u.snake_case(col) for col in df.columns]
	df = df[~(df["date"].str.contains("Sub-Total").fillna(False))] #remove daily sub-totals from the records
	df["date"] = pd.to_datetime(df["date"])#.dt.date
	st.write(df.head())
	df = df.sort_values("facility")
	st.write(df.head())
	df = df.set_index(["date", "facility"])
	
	# return df#, df_key
	return df, df_key

if __name__ == "__main__":
	main()



