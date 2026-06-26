# Customer Churn Analysis Project

## Project Overview
This project analyzes customer churn behavior using PostgreSQL, Python, Pandas, and Seaborn.

## Database Setup

### PostgreSQL Configuration
1. Create a PostgreSQL database:
   ```sql
   CREATE DATABASE telco_churn;
   ```

2. Create the telco_customers table:
   ```sql
   DROP TABLE IF EXISTS telco_customers;
   CREATE TABLE telco_customers (
       customerID VARCHAR(20),
       gender VARCHAR(10),
       tenure INT,
       monthlyCharges FLOAT,
       totalCharges FLOAT,
       churn VARCHAR(10)
   );
   ```

3. Import data from CSV:
   ```sql
   COPY telco_customers FROM '/path/to/telco_customers_CSV.csv' WITH (FORMAT csv, HEADER true);
   ```

### Environment Variables
Create a `.env` file in the project root (copy from `.env.example`):
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=telco_churn
DB_USER=postgres
DB_PASSWORD=your_password_here
```

## Week 1 Progress

### Day 1
- GitHub repository setup
- Project structure creation
- Installed PostgreSQL and Python libraries

### Day 2
- Created PostgreSQL database
- Created telco_customers table
- Imported Telco dataset

### Day 3
- Performed SQL exploratory analysis
- Executed churn-related queries

### Day 4
- Loaded dataset in Jupyter Notebook
- Performed Exploratory Data Analysis (EDA)

### Day 5
- Generated churn distribution chart
- Analyzed contract type vs churn
- Analyzed tenure vs churn

### Day 6
- Analyzed monthly charges vs churn
- Handled missing values
- Converted data types

### Day 7
- Correlation analysis
- Saved cleaned dataset

## Tools Used
- PostgreSQL
- Python
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Streamlit
- FastAPI
- Git
- GitHub
- VS Code

## How to Run

### Prerequisites
- PostgreSQL installed and running
- Python 3.8+

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (create `.env` file):
   ```bash
   cp .env.example .env
   # Edit .env with your PostgreSQL credentials
   ```

3. Set up PostgreSQL database:
   - Execute queries from `data/sqlanalysis_queries.sql`
   - Import data into `telco_customers` table

4. Run the Streamlit dashboard:
   ```bash
   streamlit run dashboard/dashboard.py
   ```

5. Run the API server:
   ```bash
   uvicorn api.app:app --reload
   ```

### API Endpoints
- `GET /` - API status
- `GET /stats` - Get churn statistics from PostgreSQL
- `POST /predict` - Predict churn for a customer

## Project Components
- `notebooks/01_EDA.ipynb`: exploratory data analysis and visualization
- `notebooks/02_model_building.ipynb`: churn model training and evaluation
- `dashboard/dashboard.py`: Streamlit churn prediction dashboard
- `api/app.py`: FastAPI churn prediction API
- `src/predict.py`: shared model input preparation helper
- `src/database.py`: PostgreSQL connection and data loading utility
- `models/churn_rf_model.pkl`: serialized Random Forest churn model
- `data/processed_churn_data.csv`: cleaned churn dataset
- `data/sqlanalysis_queries.sql`: SQL queries for database setup

## Notes
- The project now uses **PostgreSQL** for data storage and retrieval
- The API accepts customer feature input and returns churn probability
- The dashboard loads data from PostgreSQL (with CSV fallback if DB unavailable)
- All notebooks automatically connect to PostgreSQL on startup
- If PostgreSQL is unavailable, the system falls back to CSV files
