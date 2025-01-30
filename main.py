print("hello world")

csv_folder_path = "./docs/other_files/csv/"

import os

if os.path.exists(os.path.join(csv_folder_path, "Employee_Details.csv")):
    print("yow")
