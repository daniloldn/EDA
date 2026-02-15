from typing import List

import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go



def win_home_away() -> alt.Chart:
    """Build a layered bar chart comparing GSW home/away wins to league averages."""

    # Pull Golden State and comparison data
    df = pd.read_csv("data/clean_data/clean.csv")
    df_others = pd.read_csv("data/clean_data/clean_others.csv")

    # GSW win totals by venue
    wins = df.groupby(by="home").agg(
        win_total=("win", "sum"),
        total_games=("home", "count"),
    ).reset_index()
    wins["win_pct"] = wins["win_total"] / wins["total_games"]
    wins["home"] = wins["home"].apply(lambda x: "Home" if x == 1 else "Away")

    # League win rates when playing at home
    wins_home = (
        df_others.groupby("team_abbreviation_home")
        .agg(
            win_total=("win", "sum"),
            total_games=("win", "size"),
        )
        .reset_index()
    )
    wins_home["win_pct_home"] = wins_home["win_total"] / wins_home["total_games"]

    # Aggregate league-wide baseline
    home_win_pct = df_others["win"].mean()
    away_win_pct = 1 - home_win_pct
    avg_table = pd.DataFrame(
        {
            "location": ["Home", "Away"],
            "win_pct": [home_win_pct, away_win_pct],
        }
    )

    # Stack GSW and league rows for plotting
    gsw_view = wins.assign(group="GSW")[["group", "home", "win_pct"]]
    nba_view = avg_table.assign(group="NBA Avg").rename(columns={"location": "home"})
    combined = pd.concat([gsw_view, nba_view], ignore_index=True)

    layered_chart = (
        alt.Chart(combined)
        .mark_bar()
        .encode(
            x=alt.X("home:N", title="Away / Home"),
            xOffset=alt.XOffset("group:N"),
            y=alt.Y("win_pct:Q", title="Win Percentage"),
            color=alt.Color("group:N", title="Split"),
            tooltip=["group", "home", alt.Tooltip("win_pct:Q", format=".0%")],
        )
    )
    return layered_chart

def shot_efficiency() -> List[go.Figure]:
    """Create paired scatter plots for GSW shooting splits at home and on the road."""

    # Base data for both views
    df = pd.read_csv("data/clean_data/clean.csv")

    # Games hosted by Golden State
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
    #win pct below 45 degree line
    home_win_shot_better = ((gsw_home["fg_pct_home"] > gsw_home["fg_pct_away"]) & (gsw_home["win"] == 1)).sum()
    home_win_pct_shot_better = round(home_win_shot_better / (gsw_home["fg_pct_home"] > gsw_home["fg_pct_away"]).sum(), 2) *100
    home_win_shot_worse = ((gsw_home["fg_pct_home"] < gsw_home["fg_pct_away"]) & (gsw_home["win"] == 1)).sum()
    home_win_pct_shot_worse = round(home_win_shot_worse / (gsw_home["fg_pct_home"] < gsw_home["fg_pct_away"]).sum(), 2) *100
    

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

    fig.update_layout(title="GSW (Home) vs Away Shooting", xaxis_title="GSW FG%", yaxis_title="Other team FG%")

    # Games played away from Chase Center
    gsw_away = df[df["team_abbreviation_home"] != "GSW"].copy()
    gsw_away["win_flag"] = gsw_away["win"].map({1: "1", 0: "0"})

    #win pct away
    away_win_shot_better = ((gsw_away["fg_pct_home"] < gsw_away["fg_pct_away"]) & (gsw_away["win"] == 1)).sum()
    away_win_pct_shot_better = round(away_win_shot_better / (gsw_away["fg_pct_home"] < gsw_away["fg_pct_away"]).sum(), 2) *100
    away_win_shot_worse = ((gsw_away["fg_pct_home"] > gsw_away["fg_pct_away"]) & (gsw_away["win"] == 1)).sum()
    away_win_pct_shot_worse = round(away_win_shot_worse / (gsw_away["fg_pct_home"] > gsw_away["fg_pct_away"]).sum(), 2) *100
    

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

    fig2.update_layout(title="GSW (Away) vs Home Shooting", xaxis_title="GSW FG%", yaxis_title="Other team FG%")
    return [fig, fig2, home_win_pct_shot_better,home_win_pct_shot_worse, away_win_pct_shot_better, away_win_pct_shot_worse]