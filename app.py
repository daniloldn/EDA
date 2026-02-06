import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import altair as alt

#page config
st.set_page_config(page_title="GSW Dashboard", layout="wide")

st.title("GSW 2022 Analysis")

st.subheader("Performance during the regular season")

#getting data
df = pd.read_csv("data/clean_data/clean.csv")
df_others = pd.read_csv("data/clean_data/clean.csv")


#data on win pct for home and away for GSW and rest
wins = df.groupby(by = "home").agg(
    win_total = ("win","sum"),
    total_games = ("home", "count")
).reset_index()
wins["win_pct"] = wins["win_total"]/wins["total_games"]

wins_chart = alt.Chart(wins).mark_bar().encode(
    x=alt.X("home:N", title="Home Flag (1=Home)"),
    y=alt.Y("win_pct:Q", title="Win Percentage"),
    tooltip=["home", "win_total", "total_games", alt.Tooltip("win_pct:Q", format=".0%")],
).properties(width="container", height=320)


#win pct for the rest of the nba: 
wins_home = (
    df.groupby("team_abbreviation_home")
      .agg(
          win_total=("win", "sum"),
          total_games=("win", "size"),
      )
      .reset_index()
)

wins_home["win_pct_home"] = wins_home["win_total"] / wins_home["total_games"]
#avg for the nba
home_win_pct = df["win"].mean()
away_win_pct = 1 - home_win_pct

avg_table = pd.DataFrame({
    "location": ["1", "0"],
    "win_pct": [home_win_pct, away_win_pct],
})

# Plot bar chart
# Build one tidy DataFrame with both views
gsw_view = wins.assign(group="GSW")[["group", "home", "win_pct"]]
nba_view = avg_table.assign(group="NBA Avg").rename(
    columns={"location": "home"}  # so both use the same field name
)
combined = pd.concat([gsw_view, nba_view], ignore_index=True)

layered_chart = (
    alt.Chart(combined)
    .mark_bar()
    .encode(
        x=alt.X("home:N", title="Away / Home"),
        xOffset=alt.XOffset("group:N"),          # offset bars within each x bucket
        y=alt.Y("win_pct:Q", title="Win Percentage"),
        color=alt.Color("group:N", title="Split"),
        tooltip=["group", "home", alt.Tooltip("win_pct:Q", format=".0%")],
    )
)

#formating for graph allocation 
top_col1, top_col2 = st.columns([1, 1])
#plots

with top_col1:
    st.subheader("Home vs Away Wins (GSW vs NBA)")
    st.altair_chart(layered_chart, use_container_width=True)
    st.markdown("The GSW where better than the NBA in both Away and Home games, this is important as to win a series you need to win at least 1 game away if you do not have homecourt advantage. In years the GSW have struggled in the playoffs there were not a great road team")

# scatter plot
gsw_home = df[df["team_abbreviation_home"] == "GSW"].copy()
gsw_home["win_flag"] = gsw_home["win"].map({1: "1", 0: "0"})

fig = px.scatter(
    gsw_home,
    x="fg_pct_home",
    y="fg_pct_away",
    color="win_flag",
    color_discrete_map={"1": "#1f77b4", "0": "#ff7f0e"},
    category_orders={"win_flag": ["1", "0"]},
    labels={"fg_pct_home": "Home FG%", "fg_pct_away": "Away FG%", "win_flag": "Win"},
)

diag_min = min(gsw_home["fg_pct_home"].min(), gsw_home["fg_pct_away"].min())
diag_max = max(gsw_home["fg_pct_home"].max(), gsw_home["fg_pct_away"].max())
fig.add_shape(
    type="line",
    x0=diag_min,
    y0=diag_min,
    x1=diag_max,
    y1=diag_max,
    line=dict(color="#7f7f7f", dash="dash"),
)

fig.update_layout(title= "GSW Home vs Away Shooting", xaxis_title="GSW FG%", yaxis_title="Other team FG%")

gsw_away = df[df["team_abbreviation_home"] != "GSW"].copy()
gsw_away["win_flag"] = gsw_away["win"].map({1: "1", 0: "0"})

fig2 = px.scatter(
    gsw_away,
    x="fg_pct_away",
    y="fg_pct_home",
    color="win_flag",
    color_discrete_map={"1": "#1f77b4", "0": "#ff7f0e"},
    category_orders={"win_flag": ["1", "0"]},
    labels={"fg_pct_home": "Home FG%", "fg_pct_away": "Away FG%", "win_flag": "Win"},
)

diag_min = min(gsw_away["fg_pct_home"].min(), gsw_away["fg_pct_away"].min())
diag_max = max(gsw_away["fg_pct_home"].max(), gsw_away["fg_pct_away"].max())
fig2.add_shape(
    type="line",
    x0=diag_min,
    y0=diag_min,
    x1=diag_max,
    y1=diag_max,
    line=dict(color="#7f7f7f", dash="dash"),
)

fig2.update_layout(title= "GSW Away vs Home Shooting", xaxis_title="GSW FG%", yaxis_title="Other team FG%")

st.subheader("Home vs Away Shot Efficieny for GSW")
scatter_col1, scatter_col2 = st.columns(2)
with scatter_col1:
    st.plotly_chart(fig, use_container_width=True)
with scatter_col2:
    st.plotly_chart(fig2, use_container_width=True)

