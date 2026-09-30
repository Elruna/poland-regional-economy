import pandas as pd, sqlite3

con = sqlite3.connect("data/poland.db")
df = pd.read_sql("select * from fact_indicator", con)
wide = df.pivot_table(index=["region","year"], columns="indicator", values="value").reset_index()

y0, y1 = wide.year.min(), wide.year.max()
n = y1 - y0

# 1. real wage growth (CAGR) per region
a = wide[wide.year==y0].set_index("region")["wage_real"]
b = wide[wide.year==y1].set_index("region")["wage_real"]
cagr = ((b/a)**(1/n) - 1) * 100
print("\nReal wage CAGR %, by region:\n", cagr.sort_values(ascending=False).round(2))

# 2. sigma convergence: coefficient of variation per year
cv = wide.groupby("year")["wage_real"].agg(lambda s: s.std()/s.mean()*100)
print("\nCoefficient of variation of real wages by year (%):\n", cv.round(2))

# 3. wages vs unemployment: Spearman within each year (rank, then Pearson)
print("\nSpearman wage_real vs unemployment, per year:")
for y, g in wide.groupby("year"):
    rho = g["wage_real"].rank().corr(g["unemployment"].rank())
    print(y, round(rho, 2))

# 4. unemployment first vs last year
print("\nUnemployment", y0, "vs", y1)
print(wide[wide.year.isin([y0, y1])].pivot(index="region", columns="year", values="unemployment").round(1))

