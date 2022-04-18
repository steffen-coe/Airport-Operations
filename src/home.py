import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def write(data):
	df = data
	# categories = ["itin_carrier" ,"itin_taxi", "itin_ga", "itin_military", "lcl_civil", "lcl_miltary"]
	categories = {"itin_carrier" : "Itinerant Air Carrier", "itin_taxi" : "Itinerant Air Taxi", "itin_ga" : "Itinerant General Aviation", "itin_military" : "Itinerant Military", "lcl_civil" : "Local Civil", "lcl_miltary" : "Local Military"}
	
	st.title("Operations at PAE and MWH Airports 🛩️🌎")
	
	st.write("Explore the number of operations (take-offs and landings) at each of the following three airports. Have fun! 💡")
	st.write("+ Grant County (Moses Lake) Airport (MWH)\n + Paine Field/Snohomish County Airport (PAE)\n + Seattle-Tacoma International Airport (SEA)")
	
	st.write("Data is taken from the [FAA's Operations Network (OPSNET)](https://aspm.faa.gov/opsnet/sys/Airport.asp), reporting counts of airport operations as recorded by the Air Traffic Activity System (ATADS).")
		
	# aggregation by day/month/year
	options = ["Day", "Month", "Year"]
	aggregation = st.radio('Aggregate data by:', options, index=options.index("Month"))
	
	
	fac = st.selectbox("Airport:", df.index.levels[1].to_list())
	
	df_fac = df.loc[(slice(None), fac), :]
	df_fac.index = df_fac.index.droplevel("facility")
	
	# show totals or grouped by category
	options = ["By category", "Total"]
	chart = st.radio("Show total number of operations or by operation category", options, index=options.index("By category"))
	
	fig = go.Figure()
	
	layout = dict(
		height=600, 
		xaxis_title = "Date", 
		yaxis_title = "Number of operations", 
		xaxis = dict(
			rangeselector = dict(
				buttons=list([
					dict(count=1,
						 label="1m",
						 step="month",
						 stepmode="backward"),
					dict(count=6,
						 label="6m",
						 step="month",
						 stepmode="backward"),
					dict(step="all")
				])
			),
			rangeslider = dict(
				visible = True
			),
			type = "date"
		), 
		barmode="stack", 
		showlegend=True, 
		hovermode='x unified', 
	)
	fig.update_layout(layout)
	# fig.update_xaxes(ticklabelmode="period")
	
	if aggregation == "Day":
			dff = df_fac
	elif aggregation == "Month":
		df_fac_byM = df_fac.resample("M").sum()
		df_fac_byM.index = [pd.to_datetime("%d-%d-01"%(datetime.year, datetime.month)) for datetime in df_fac_byM.index]
		dff = df_fac_byM
		fig.update_layout(xaxis=dict(dtick="M1"))
	elif aggregation == "Year":
		df_fac_byY = df_fac.resample("Y").sum()
		df_fac_byY.index = [pd.to_datetime("%d-01-01"%(datetime.year)) for datetime in df_fac_byY.index]
		dff = df_fac_byY
		fig.update_layout(xaxis=dict(tickformat = "%Y", dtick="M12"))
	
	if chart == "By category":
		for cat in categories.keys():
			fig.add_trace(go.Bar(x=dff.index, y=dff[cat], name=categories[cat]))
	elif chart == "Total":
		fig.add_trace(go.Bar(x=dff.index, y=dff["total_ops"], name="Total no. of operations"))

	st.plotly_chart(fig, sharing="streamlit", use_container_width=True)
	
