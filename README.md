# Reliability Test Timeline Generator

This is a Streamlit tool that auto-generates reliability test timelines based on selected processes, a start date, and predefined turnaround times (TAT) for each sub-process.
It is designed to simplify QAWR test planning, highlight key milestones, and produce clear Gantt-style charts for tracking progress.

## 🚀 Getting Started

Run the app locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) to view it in your browser.

## ✨ Features

* Interactive Streamlit interface
* Auto-generated Gantt chart using Plotly Express
* Predefined reliability test processes:
* Custom color coding for Pretest, VI, Readpoints, Shipments, and Stress steps
* Highlights day-by-day progress with a secondary top x-axis (Day Count)
* No gaps between sub-processes for a continuous timeline flow
  
## 📂 Project Structure

* `reliability_timeline.py` – Main Streamlit app
* `requirements.txt` – Dependencies (Streamlit, Pandas, Plotly)
* `README.md` – Project documentation
