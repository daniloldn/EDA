import streamlit as st
from src.plots import win_home_away, shot_efficiency, correlation
from src.shot_efficiency import linear_reg

#page config
st.set_page_config(page_title="GSW Dashboard", layout="wide")

st.title("GSW 2022 Performance & Shot Efficiency Dashboard")

st.markdown(
    """
This exploratory data analysis (EDA) examines how shooting efficiency influenced game outcomes for the 2022 Golden State Warriors, with a focus on differences between home and away performance.

The objective is to identify key drivers of shot efficiency and understand how efficiency translates into winning games."""
)

st.subheader("Performance during the regular season")


#formating for graph allocation 
top_col1, top_col2 = st.columns([1, 1])
#plots

with top_col1:
    st.subheader("Home vs Away Wins (GSW vs NBA)")
    st.altair_chart(win_home_away(), use_container_width=True)
    st.markdown("The Golden State Warriors performed better than the NBA average in both home and away games. This is particularly important in a playoff context, as winning a series without home-court advantage requires at least one away win. Historically, in seasons where the Warriors have struggled in the playoffs, their road performance has been noticeably weaker.")


st.subheader("Home vs Away Shot Efficiency for GSW")
scatter_col1, scatter_col2 = st.columns(2)
with scatter_col1:
    st.plotly_chart(shot_efficiency()[0], use_container_width=True)
with scatter_col2:
    st.plotly_chart(shot_efficiency()[1], use_container_width=True)


st.markdown(
    f"""
The scatter plots compare the Warriors’ field goal percentage to their opponents’ field goal percentage, separated by home and away games. Points below the diagonal line indicate games where GSW shot more efficiently than their opponent, while points above indicate the opposite.

The data shows that when the Warriors shoot more efficiently than their opponent, they win approximately {shot_efficiency()[2]}% of home games and {shot_efficiency()[4]}% of away games. In contrast, when they shoot less efficiently, their win rate drops to around {shot_efficiency()[3]}% at home and {shot_efficiency()[5]}% away.

This suggests that relative shooting efficiency is a key determinant of game outcomes. Therefore, to better understand what drives winning performance, the next step is to analyse the factors that contribute to shot efficiency."""
)


st.subheader("The determinants of shot efficiency")

st.markdown(
    """
A natural next step is to examine the correlations between key covariates and shot efficiency"""
)

corr_col1, corr_col2 = st.columns(2)
with corr_col1:
    st.plotly_chart(correlation()[0], use_container_width=True)
with corr_col2:
    st.plotly_chart(correlation()[1], use_container_width=True)

st.markdown(
    """
    Correlation analysis provides initial insight into the variables associated with shot efficiency. One notable pattern is that momentum-related variables, such as largest lead, appear to play a stronger role in away games than in home games.

Shot selection also seems relevant: fast break opportunities are typically associated with higher conversion rates than three-point attempts. Additionally, higher assist numbers suggest better ball movement, which likely leads to more open and higher-quality shots.

However, correlations do not account for the joint influence of multiple covariates. To address this limitation, a multivariate linear regression is estimated. By the Frisch–Waugh–Lovell (FWL) theorem, the coefficients can be interpreted as the partial effect of each variable after controlling for the others.
    """
)

results_home, results_away = linear_reg()

reg_col1, reg_col2 = st.columns(2)
with reg_col1:
    st.subheader("Home games")
    st.markdown(f"""```
{results_home.summary().as_text()}
```""", unsafe_allow_html=False)
with reg_col2:
    st.subheader("Away games")
    st.markdown(f"""```
{results_away.summary().as_text()}
```""", unsafe_allow_html=False)
    
st.markdown(
    """
When controlling for other covariates, many of the previously observed correlations lose statistical significance, suggesting that bivariate relationships may be driven by confounding factors.

For home games, one interesting relationship is the positive association between opponent points in the paint and GSW shot efficiency. One possible interpretation is that when opponents focus on interior scoring, they may be slower to reset defensively, allowing the Warriors to generate higher-quality offensive possessions.

The model explains a large proportion of the variation in shot efficiency (high R²), although the extremely small eigenvalues indicate potential multicollinearity, so coefficient estimates should be interpreted with caution. 


For away games, plus-minus appears more relevant, suggesting that overall team performance and game momentum play a larger role in shooting efficiency on the road. This is consistent with the idea that away environments amplify the importance of momentum and in-game performance dynamics.
   """
)

st.subheader("Key Takeaways")
st.markdown(
    """
Shooting more efficiently than opponents is strongly linked to winning, especially in away games

Ball movement (assists) and shot quality appear to be key drivers of efficiency

Momentum-related metrics play a larger role in away performance

Multivariate analysis shows that many simple correlations weaken once other factors are controlled for, highlighting the importance of proper statistical modelling"""
)