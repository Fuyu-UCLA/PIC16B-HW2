import pandas as pd

results = pd.read_csv("results.csv")

df = results.groupby("movie_or_TV_name").count()