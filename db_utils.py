from sqlalchemy import create_engine 
from sqlalchemy import text

def connect_postgres(user, password, host, port, dbname):
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")
    return engine

def create_schema_if_not_exists(engine, schema_name):
    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        print(f"Schema '{schema_name}' created or already exists.")

def write_to_db(df, table_name, engine, schema, if_exists='replace', chunksize=10000):
    df.to_sql(table_name, engine, schema=schema, if_exists=if_exists, index=False, chunksize=chunksize)
    print(f"Load '{table_name}' Done.")


