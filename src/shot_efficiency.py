import statsmodels.formula.api as smf
import pandas as pd


def linear_reg():
    # Base data for both views
    df = pd.read_csv("data/clean_data/clean.csv")
    gsw_home = df[df["team_abbreviation_home"] == "GSW"].copy()
    gsw_home = gsw_home.select_dtypes(include="number")
    
    #dropping columns and correlation
    gsw_home = gsw_home.drop(
    columns=["min", "home", "win", "video_available_home", "video_available_away", "pts_home", 
    "fgm_home", "fg3_pct_home", "fg3m_home"],
    errors="ignore",
    )
    #home moodel
    target = "fg_pct_home"


    corr_with_target = (
    gsw_home.corr(numeric_only=True)[target]
    .drop(target)
    .sort_values(key=lambda s: s.abs(), ascending=False)
    )

    top_n = 15
    corr_top = corr_with_target.head(top_n).reset_index()
    corr_top.columns = ["feature", "corr"]
    #away model
    gsw_away = df[df["team_abbreviation_home"] != "GSW"].copy()

    gsw_away = gsw_away.select_dtypes(include="number")
    
    #dropping columns and correlation
    gsw_away = gsw_away.drop(
    columns=["min", "home", "win", "video_available_home", "video_available_away", "pts_away", 
    "fgm_away", "fg3_pct_away", "fg3m_away"],
    errors="ignore",
    )

    #fig 1
    target = "fg_pct_away"


    corr_with_target_away = (
    gsw_away.corr(numeric_only=True)[target]
    .drop(target)
    .sort_values(key=lambda s: s.abs(), ascending=False)
    )

    top_n = 15
    corr_top_away = corr_with_target_away.head(top_n).reset_index()
    corr_top_away.columns = ["feature", "corr"]


    #model
    predictors_home = " + ".join(corr_top["feature"])
    model_home = smf.ols(f"fg_pct_home ~ {predictors_home}", data=gsw_home)
    results_home = model_home.fit()

    predictors_away = " + ".join(corr_top["feature"])
    model_away = smf.ols(f"fg_pct_home ~ {predictors_away}", data=gsw_away)
    results_away = model_away.fit()

    



    return [results_home, results_away]