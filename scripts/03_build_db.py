import pandas as pd, sqlite3

w = pd.read_csv("data/wage_nominal.csv")
u = pd.read_csv("data/unemployment.csv")
c = pd.read_csv("data/cpi_prev_year.csv")[["year", "value"]].rename(columns={"value": "cpi"})

# region names: BDL uses uppercase, make them tidy
for d in (w, u):
    d["region"] = d["region"].str.title()

# price index chained to 2015 = 1.0
c = c.sort_values("year").reset_index(drop=True)
c["price_index"] = (c["cpi"] / 100).cumprod() / (c.loc[0, "cpi"] / 100)

w = w.merge(c[["year", "price_index"]], on="year", how="left")
w["real_wage"] = w["value"] / w["price_index"]

# long format
long = pd.concat([
    w.assign(indicator="wage_nominal")[["unit_id","region","year","indicator","value"]],
    w.assign(indicator="wage_real", value=w["real_wage"])[["unit_id","region","year","indicator","value"]],
    u.assign(indicator="unemployment")[["unit_id","region","year","indicator","value"]],
])

print("Missing values:\n", long[long["value"].isna()])   
long = long.dropna(subset=["value"])

con = sqlite3.connect("data/poland.db")
long.to_sql("fact_indicator", con, if_exists="replace", index=False)
con.close()
print("Saved", len(long), "rows")