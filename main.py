import pandas as pd 
from loader import load_data, extract_store_name
from cleaner import drop, normalize_names,convert_dtypes,normalize_tables
from db_utils import connect_postgres,create_schema_if_not_exists, write_to_db

def main():

    # 1. Load and preprocessing
    file_path = "C:\\Users\\DELL\\OneDrive\\Desktop\\[HMD TEST] - BI- THIÊN PHỤNG\\data_sales.csv"
    data = load_data(file_path)
    data = extract_store_name(data)
    data = drop(data)
    data = normalize_names(data)
    data = convert_dtypes(data)

    df_store, df_category, df_vendor, df_sales = normalize_tables(data)


    # 2. Connect PostgreSQL
    engine = connect_postgres(
        user='postgres',
        password='phung',
        host='localhost',
        port=5432,
        dbname='DWH'
    )

    # 3. Create schema 
    create_schema_if_not_exists(engine, 'sales_data')

    # 3. Write data to database 
    write_to_db(df_store, "store_dim", engine,'sales_data')
    write_to_db(df_category, "category_dim", engine,'sales_data')
    write_to_db(df_vendor, "vendor_dim", engine,'sales_data')
    write_to_db(df_sales, "sales", engine,'sales_data')


if __name__ == '__main__':
    main()
