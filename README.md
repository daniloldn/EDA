# GSW Shot Efficiency EDA

This project is an exploratory data analysis of the 2021-22 Golden State Warriors that focuses on how shooting efficiency shifts between home and away games and how those shifts relate to winning. A Streamlit dashboard (app.py) pulls pre-cleaned NBA game data and surfaces interactive visuals plus an on-the-fly linear regression summary.

## Key Features
- **Home vs. away context** – layered Altair bars show how GSW win rates compare to league-wide home/away baselines.
- **Shot efficiency scatter plots** – Plotly charts contrast GSW field-goal percentage with opponents’ efficiency and compute win rates when the Warriors shoot better or worse.
- **Determinants of efficiency** – Top correlations and statsmodels OLS results highlight which metrics (assists, pace, momentum, etc.) best explain shooting performance in each setting.

## Data
- Cleaned data lives under data/clean_data/ (clean.csv for GSW games, clean_others.csv for the comparison set) and feeds every visualization.
- CSVs are assumed to already be prepared; no scraping code is included here.

## Getting Started
1. Create and activate a Python 3.10+ environment.
2. Install requirements: `pip install -r requirements.txt`.
3. Launch the dashboard from the project root with `streamlit run app.py`.
4. Interact with the three panels to explore win splits, shot efficiency, correlations, and the regression output (rendered as plain text inside Streamlit).

## Repository Layout
- app.py – Streamlit UI wiring plus narrative context.
- src/plots.py – All Altair/Plotly figures and supporting win-rate calculations.
- src/shot_efficiency.py – Helper that filters features and fits separate OLS models for home and away contexts.
- data/ – Clean CSV inputs (not tracked here beyond sample paths).
- eda.ipynb – Notebook used during exploratory work (not required to run the app).


