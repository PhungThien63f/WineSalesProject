import pandas as pd 


def drop(data):
    data = data.drop(columns= {'Vendor Number','City Name','City Code','Store Number'})
    return data 

def normalize_names(data):
    data = data.rename(columns={
        "Date": "date",
        "Store Name": "store_name",
        "City":"city_name",
        "Category Name": "category_name",
        "Vendor Name": "vendor_name",
        "Bottles Sold": "bottles_sold"
    })
    return data 


def convert_dtypes(data):
    #date
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'], errors='coerce')

    # numeric
    int_cols = ['bottles_sold']
    for col in int_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').astype('Int64')

    # category
    str_cols = ['store_name', 'city_name', 'category_name', 'vendor_name']
    for col in str_cols:
        if col in data.columns:
            data[col] = data[col].astype(str)

    return data

def normalize_tables(data):
    # store_dim
    df_store = data[['store_name', 'city_name']].drop_duplicates().reset_index(drop=True)
    df_store['store_id'] = df_store.index + 1

    # category_dim
    df_category = data[['category_name']].dropna().drop_duplicates().reset_index(drop=True)
    df_category['category_id'] = df_category.index + 1

    # vendor_dim
    df_vendor = data[['vendor_name','city_name']].dropna().drop_duplicates().reset_index(drop=True)
    df_vendor['vendor_id'] = df_vendor.index + 1

     # sales
    df_sales = data[['date', 'store_name', 'city_name', 'category_name', 'vendor_name', 'bottles_sold']]
    df_sales = df_sales.merge(df_store, on=['store_name', 'city_name'], how='left')
    df_sales = df_sales.merge(df_category, on='category_name', how='left')
    df_sales = df_sales.merge(df_vendor, on=['vendor_name', 'city_name'], how='left', suffixes=('', '_vendor'))
    df_sales['sale_id'] = df_sales.index + 1
    df_sales = df_sales[['sale_id', 'date', 'store_id', 'category_id', 'vendor_id', 'bottles_sold']]

    return df_store, df_category, df_vendor, df_sales





