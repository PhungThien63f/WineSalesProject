import pandas as pd 
import numpy as np 

def load_data(file_path):
     return pd.read_csv(file_path)

# split store_name 
import pandas as pd

def extract_store_name(data):
    def split_store_name(store_name):
        if pd.isnull(store_name):
            return None, None, None

        if '#' in store_name and '/' in store_name:
            try:
                name_part, city_part = store_name.split('#', 1)
                city_code, city_name = city_part.split('/', 1)
                return name_part.strip(), city_code.strip(), city_name.strip()
            except ValueError:
                return store_name.strip(), None, None
        elif '/' in store_name:
            try:
                name_part, city_name = store_name.split('/', 1)
                return name_part.strip(), None, city_name.strip()
            except ValueError:
                return store_name.strip(), None, None
        elif '#' in store_name:
            try:
                name_part, city_code = store_name.split('#', 1)
                return name_part.strip(), city_code.strip(), None
            except ValueError:
                return store_name.strip(), None, None
        else:
            return store_name.strip(), None, None

    extracted = data['Store Name'].apply(split_store_name)
    extracted_df = pd.DataFrame(extracted.tolist(), columns=["Store Name", "City Code", "City Name"])

    data["Store Name"] = extracted_df["Store Name"]
    data["City Code"] = extracted_df["City Code"]
    data["City Name"] = extracted_df["City Name"]

    return data

