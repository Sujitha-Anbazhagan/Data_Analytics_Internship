# Customer Churn Analysis Project

## Project Overview
This project analyzes customer churn behavior using SQL, PostgreSQL, Python, Pandas, and Seaborn.

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
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit dashboard:
   ```bash
   streamlit run dashboard/dashboard.py
   ```
3. Run the API server:
   ```bash
   uvicorn api.app:app --reload
   ```

## Project Components
- `notebooks/01_EDA.ipynb`: exploratory data analysis and visualization
- `notebooks/02_model_building.ipynb`: churn model training and evaluation
- `dashboard/dashboard.py`: Streamlit churn prediction dashboard
- `api/app.py`: FastAPI churn prediction API
- `src/predict.py`: shared model input preparation helper
- `models/churn_rf_model.pkl`: serialized Random Forest churn model
- `data/processed_churn_data.csv`: cleaned churn dataset

## Notes
- The API accepts customer feature input and returns churn probability.
- The dashboard loads the same saved model and predicts churn from user inputs.
- Duplicate or unused raw data files were removed to keep the repo clean.
