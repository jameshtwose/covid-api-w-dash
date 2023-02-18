import pandas as pd
import numpy as np
from functools import lru_cache
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@lru_cache(maxsize=32)
def get_data():
    df = (pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
            .assign(**{"date": lambda x: pd.to_datetime(x["date"]).dt.date}))
    return df.loc[:, ["date", "continent", "location", "new_cases", "new_deaths", "new_tests"]].replace(np.nan, 0)


@app.get("/")
def read_root():
    df = get_data()
    return {"available_columns": df.columns.tolist()}


@app.get("/head")
def get_head():
    head_df = get_data().head(5)
    return head_df.to_dict()


@app.get("/groupby_totals")
def get_groupby_totals():
    df = get_data()
    df_groupby_totals = df.groupby(["location"]).sum()
    return df_groupby_totals.to_dict()


@app.get("/groupby_descriptives")
def get_groupby_descriptives():
    df = get_data()
    df_groupby_descriptives = (df.loc[:, ["location", "new_cases", "new_deaths", "new_tests"]]
                               .groupby(["location"])
                               .agg(["min", "mean", "median", "max"])
                               .dropna())
    df_groupby_descriptives.columns = [
        "_".join(x) for x in df_groupby_descriptives.columns]
    return df_groupby_descriptives.reset_index().to_dict()


@app.get("/locations/{location_id}")
def get_location_time_seris(location_id: str):
    df = get_data()
    df_location = df.loc[df["location"] == location_id, :]
    return df_location.to_dict()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)