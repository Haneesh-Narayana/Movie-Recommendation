import pandas as pd
read_file=pd.read_csv(r"C:\Users\hanee\Downloads\census+income\adult.data")
read_file.to_csv(r"C:\Users\hanee\Downloads\census+income\adult.csv",index=False)
