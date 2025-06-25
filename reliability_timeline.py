import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide")  # Ensures wide layout

# Define the durations for each process and sub-process
durations = {
    "Temp Cycle J/K": [
        ("Pretest", 3),
        ("VI", 1),
        ("250cyc", 7),
        ("Readpoint", 3),
        ("500cyc", 7),
        ("Readpoint", 3),
        ("750cyc", 7),
        ("Readpoint", 3),
        ("1000cyc", 7),
        ("Readpoint", 3),
        ("VI", 1),
        ("1250cyc", 7),
        ("Readpoint", 3),
    ],
    "Random Vibration": [
        ("Pretest", 3),
        ("Precon", 10),
        ("Custom/K9 Approval", 15),
        ("Shipment", 2),
        ("RV", 5),
        ("Shipment", 2),
        ("Post Test", 3),
    ],
    "HAST 110C": [
        ("Pretest", 3),
        ("VI", 1),
        ("CM", 1),
        ("HAST 96hrs", 3),
        ("Readpoint", 3),
        ("VI", 1),
        ("CM", 1),
        ("HAST 264hrs", 7),
        ("Readpoint", 3),
    ],
    "Mechanical Shock": [
        ("Pretest", 3),
        ("VI", 1),
        ("Precon", 10),
        ("Shock", 6),
        ("VI", 1),
        ("Post Test", 3),
    ],
    "Bend": [
        ("Pretest", 3),
        ("Precon", 10),
        ("Bend", 6),
        ("Post Test", 3),
    ],
    "Torsion": [
        ("Pretest", 3),
        ("Precon", 10),
        ("Torsion", 6),
        ("Post Test", 3),
    ],
    "Vibration Temp Cycle": [
        ("Pretest", 3),
        ("VTC", 7),
        ("Post Test", 3),
    ]
}

# Define custom colors for sub-processes
custom_colors = {
    "Pretest": "lightgreen",
    "Readpoint": "lightgreen",
    "Post Test": "lightgreen",
    "VI": "lightblue",
    "250cyc": "peachpuff",
    "500cyc": "peachpuff",
    "750cyc": "peachpuff",
    "1000cyc": "peachpuff",
    "1250cyc": "peachpuff",
    "Precon": "peachpuff",
    "RV": "peachpuff",
    "Shock": "peachpuff",
    "Bend": "peachpuff",
    "HAST 96hrs": "peachpuff",
    "HAST 264hrs": "peachpuff",
    "VTC": "peachpuff",
    "CM": "lightpurple",
    "Custom/K9 Approval": "lightgreen",
    "Shipment": "blue"
}

# Streamlit app
st.title("Reliability Test Timeline Generator")

# Input QAWR number
qawr_number = st.text_input("Enter QAWR Number")

# Select reliability test processes
selected_processes = st.multiselect(
    "Select Reliability Test Processes",
    list(durations.keys())
)

# Input start date
start_date = st.date_input("Select Start Date")

# Generate timeline
if st.button("Generate Timeline"):
    if qawr_number and selected_processes and start_date:
        timeline = []
        current_date = start_date

        for process in selected_processes:
            process_start_date = current_date
            total_days = 0
            for sub_process, days in durations[process]:
                end_date = process_start_date + timedelta(days=days)
                timeline.append({
                    "Process": f"{process} ({total_days + days} days)",
                    "Sub-Process": sub_process,
                    "Start Date": process_start_date,
                    "End Date": end_date,
                    "Color": custom_colors.get(sub_process, "peachpuff")  # Default color if not specified
                })
                process_start_date = end_date + timedelta(days=1)  # No gap between sub-processes
                total_days += days

        # Convert timeline to DataFrame
        df_timeline = pd.DataFrame(timeline)

        # Create Gantt chart
        fig = px.timeline(
            df_timeline,
            x_start="Start Date",
            x_end="End Date",
            y="Process",
            color="Color",
            text="Sub-Process",
            title=f"Timeline for QAWR Number: {qawr_number}"
        )
        
        # Add week and day labels to x-axis
        fig.update_xaxes(
            tickformat="%d-%b",
            ticklabelmode="period",
            dtick="D1",
            tick0=start_date
        )
        fig.update_xaxes(
            tickformatstops=[
                dict(dtickrange=[None, 1000], value="%d-%b"),
                dict(dtickrange=[1000, None], value="Week %U")
            ]
        )

        fig.update_yaxes(categoryorder="total ascending")
        fig.update_traces(textposition='inside', insidetextanchor='middle')
        fig.update_layout(showlegend=False)

        # Display the Gantt chart
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Please enter QAWR number, select processes, and choose a start date.")

