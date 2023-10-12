import psycopg2
from decouple import config

conn = psycopg2.connect(
    host=config("POSTGRES_HOST"),
    port="5432",
    database="stocks_portfolio",
    user=config("POSTGRES_USER"),
    password=config("POSTGRES_PASSWORD"),
)

cur = conn.cursor()

def create_stocks_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(10) NOT NULL,
            full_name VARCHAR(255),
            shares_bought DECIMAL(10,2),
            price_per_share DECIMAL(10,2),
            total_cost DECIMAL(10,2),
            current_price DECIMAL(10,2),
            current_cost DECIMAL(10,2),
            difference DECIMAL(10,2)
        );
    """)
    conn.commit()
