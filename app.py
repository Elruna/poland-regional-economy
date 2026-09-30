import streamlit as st, pandas as pd, sqlite3, plotly.express as px

@st.cache_data
def load():
    con = sqlite3.connect("data/poland.db")
    return pd.read_sql("select * from fact_indicator", con)

df = load()
st.title("Wages and unemployment across Polish voivodeships")

names = {"wage_real": "Real wage (2015 prices, PLN)",
         "wage_nominal": "Nominal wage (PLN)",
         "unemployment": "Registered unemployment (%)"}
ind = st.selectbox("Indicator", list(names), format_func=names.get)
years = sorted(df.year.unique())
year = st.slider("Year", int(years[0]), int(years[-1]), int(years[-1]))

d = df[(df.indicator == ind) & (df.year == year)].sort_values("value")
st.plotly_chart(px.bar(d, x="value", y="region", orientation="h", title=f"{names[ind]}, {year}"),
                use_container_width=True)

regions = st.multiselect("Compare regions over time", sorted(df.region.unique()),
                         default=["Mazowieckie", "Podkarpackie"])
t = df[(df.indicator == ind) & (df.region.isin(regions))]
st.plotly_chart(px.line(t, x="year", y="value", color="region", markers=True),
                use_container_width=True)