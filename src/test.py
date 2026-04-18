import pandas as pd

df = pd.read_csv("data/fertilizer_data.csv")
print(df['Crop_Type'].unique())