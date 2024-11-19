import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport

dir_path = "../dataset/"

input_data = pd.read_excel(dir_path +  'Counsellor Attributes USDC-LO.xlsx')

print(input_data)

# Take a smaller sample of the dataset, e.g., 10,000 rows
#sample_df = merged_df.sample(n=10000, random_state=42)
profile = ProfileReport(input_data, title="YData Profiling Report")
profile.to_file("YData_profiling_report.html")