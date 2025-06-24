import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Define the durations for each process and sub-process
durations = {
    "Temp Cycle J/K": [
        ("Pretest", 3),
        ("VI", 1),
        ("250cyc", 6),
        ("readpoint", 3),
        ("500cyc", 6),
        ("readpoint", 3),
        ("750cyc", 6),
        ("readpoint", 3),
        ("1000cyc", 6),
        ("VI", 1),
        ("1250cyc", 6),
        ("readpoint", 3)
    ],
    "Random Vibration": [("Random Vibration", 40)],
    "HAST 110C": [("HAST 110C", 24)],
    "Mechanical Shock": [("Mechanical Shock", 24)],
    "Bend": [("Bend", 22)],
    "Torsion": [("Torsion", 22)],
    "Vibration Temp Cycle": [("Vibration Temp Cycle", 13)]
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
            for sub_process, days in durations[process]:
                end_date = current_date + timedelta(days=days)
                timeline.append({
                    "Process": process,
                    "Sub-Process": sub_process,
                    "Start Date": current_date,
                    "End Date": end_date
                })
                current_date = end_date + timedelta(days=1)  # Assuming 1 day gap between sub-processes

        # Convert timeline to DataFrame
        df_timeline = pd.DataFrame(timeline)

        # Display the timeline
        st.write(f"### Timeline for QAWR Number: {qawr_number}")
        st.table(df_timeline)
    else:
        st.error("Please enter QAWR number, select processes, and choose a start date.")