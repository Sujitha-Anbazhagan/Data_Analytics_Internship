import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()


class PostgreSQLConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish PostgreSQL connection"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", 5432),
                database=os.getenv("DB_NAME", "telco_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres123")
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("✅ PostgreSQL connection established")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise

    def load_dataframe(self, query: str) -> pd.DataFrame:
        """Execute query and return results as DataFrame"""
        try:
            df = pd.read_sql_query(query, self.conn)
            return df
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ PostgreSQL connection closed")


    def get_churn_data() -> pd.DataFrame:
        """Load churn data from PostgreSQL, otherwise use CSV"""

        try:
            db = PostgreSQLConnection()
            df = db.load_dataframe("SELECT * FROM telco_customers;")
            db.close()
            return df

        except Exception as e:
            print(f"Could not connect to PostgreSQL. Using CSV fallback: {e}")

            csv_path = "data/telco/telco_customers.csv"
            return pd.read_csv(csv_path)


    def get_churn_summary():

        try:
            db = PostgreSQLConnection()

            query = """
            SELECT churn,
                COUNT(*) as count
            FROM telco_customers
            GROUP BY churn;
            """

            df = db.load_dataframe(query)
            db.close()
            return df.to_dict("records")

        except Exception:

            df = pd.read_csv("data/telco/telco_customers.csv")

            summary = (
                df.groupby("Churn")
                .size()
                .reset_index(name="count")
            )

            return summary.to_dict("records")
