import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import altair as alt
from src.plots import win_home_away, shot_efficiency, correlation

#page config
st.set_page_config(page_title="GSW Dashboard", layout="wide")

st.title("GSW 2022 Analysis")

st.subheader("Performance during the regular season")


#formating for graph allocation 
top_col1, top_col2 = st.columns([1, 1])
#plots

with top_col1:
    st.subheader("Home vs Away Wins (GSW vs NBA)")
    st.altair_chart(win_home_away(), use_container_width=True)
    st.markdown("The Golden State Warriors performed better than the NBA average in both home and away games. This is particularly important in a playoff context, as winning a series without home-court advantage requires at least one away win. Historically, in seasons where the Warriors have struggled in the playoffs, their road performance has been noticeably weaker.")


st.subheader("Home vs Away Shot Efficieny for GSW")
scatter_col1, scatter_col2 = st.columns(2)
with scatter_col1:
    st.plotly_chart(shot_efficiency()[0], use_container_width=True)
with scatter_col2:
    st.plotly_chart(shot_efficiency()[1], use_container_width=True)


st.markdown(
    f"""
The scatter plots compare the Warriors’ field goal percentage to their opponents’ field goal percentage, separated by home and away games. Points below the diagonal line indicate games where GSW shot more efficiently than their opponent, while points above indicate the opposite.

From the data, when the Warriors shoot more efficiently than their opponent, they win approximately {shot_efficiency()[2]}% of home games and {shot_efficiency()[4]}% of away games. In contrast, when they shoot less efficiently, their win rate drops to around {shot_efficiency()[3]}% at home and {shot_efficiency()[5]}% away.

This suggests that relative shooting efficiency is a key determinant of game outcomes. Therefore, to better understand what drives winning performance, the next step is to analyse the factors that contribute to shot efficiency."""
)


st.subheader("The determinants of shot efficiency")

st.markdown(
    """
A natural next step is to look at the correlations of the the covarites with shot effiency"""
)

corr_col1, corr_col2 = st.columns(2)
with corr_col1:
    st.plotly_chart(correlation()[0], use_container_width=True)
with corr_col2:
    st.plotly_chart(correlation()[1], use_container_width=True)