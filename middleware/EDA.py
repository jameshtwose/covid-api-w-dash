# %%
import pandas as pd
# %%
df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
# %%
df_groupby_descriptives = (df.loc[:, ["location", "new_cases", "new_deaths", "new_tests"]]
                            .groupby(["location"])
                            .agg(["min", "mean", "median", "max"])
                            .dropna())
df_groupby_descriptives.columns = ["_".join(x) for x in df_groupby_descriptives.columns]
# %%
df_groupby_descriptives