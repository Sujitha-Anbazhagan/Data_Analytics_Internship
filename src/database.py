import os
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


class PostgreSQLConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish PostgreSQL connection"""
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            database=os.getenv("DB_NAME", "telco_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres123"),
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def load_dataframe(self, query: str) -> pd.DataFrame:
        return pd.read_sql_query(query, self.conn)

    def close(self):
        if self.conn:
            self.conn.close()


def get_churn_data() -> pd.DataFrame:
    """Load churn data from PostgreSQL or CSV"""

    try:
        db = PostgreSQLConnection()
        df = db.load_dataframe("SELECT * FROM telco_customers;")
        db.close()
        return df

    except Exception as e:
        print(f"Could not connect to PostgreSQL. Using CSV fallback: {e}")
        return pd.read_csv("data/processed_churn_data.csv")


def get_churn_summary():
    """Get churn summary from PostgreSQL or CSV"""

    try:
        db = PostgreSQLConnection()

        query = """
        SELECT churn,
               COUNT(*) AS count
        FROM telco_customers
        GROUP BY churn;
        """

        df = db.load_dataframe(query)
        db.close()
        return df.to_dict("records")

    except Exception as e:
        print(f"Could not connect to PostgreSQL. Using CSV fallback: {e}")

        df = pd.read_csv("data/processed_churn_data.csv")

        summary = (
            df.groupby("churn")
            .size()
            .reset_index(name="count")
        )

        return summary.to_dict("records")