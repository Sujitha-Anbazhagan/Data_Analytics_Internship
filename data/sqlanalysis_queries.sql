SELECT tablename
FROM pg_tables
WHERE schemaname = 'public';
DROP TABLE telco_customers;
CREATE TABLE telco_customers (
    customerid TEXT,
    gender TEXT,
    seniorcitizen INT,
    partner TEXT,
    dependents TEXT,
    tenure INT,
    phoneservice TEXT,
    multiplelines TEXT,
    internetservice TEXT,
    onlinesecurity TEXT,
    onlinebackup TEXT,
    deviceprotection TEXT,
    techsupport TEXT,
    streamingtv TEXT,
    streamingmovies TEXT,
    contract TEXT,
    paperlessbilling TEXT,
    paymentmethod TEXT,
    monthlycharges NUMERIC,
    totalcharges TEXT,
    churn TEXT
);
SELECT current_database();
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public';
CREATE TABLE telco_customers (
    customerid TEXT,
    gender TEXT,
    seniorcitizen INT,
    partner TEXT,
    dependents TEXT,
    tenure INT,
    phoneservice TEXT,
    multiplelines TEXT,
    internetservice TEXT,
    onlinesecurity TEXT,
    onlinebackup TEXT,
    deviceprotection TEXT,
    techsupport TEXT,
    streamingtv TEXT,
    streamingmovies TEXT,
    contract TEXT,
    paperlessbilling TEXT,
    paymentmethod TEXT,
    monthlycharges NUMERIC,
    totalcharges TEXT,
    churn TEXT
);
SELECT * FROM telco_customers LIMIT 5;
DROP TABLE IF EXISTS telco_customers;
CREATE TABLE telco_customers (
    customerID VARCHAR(20),
    gender VARCHAR(10),
    tenure INT,
    monthlyCharges FLOAT,
    totalCharges FLOAT,
    churn VARCHAR(10)
);
SELECT COUNT(*) FROM telco_customers;
SELECT COUNT(*) FROM telco_customers;
SELECT * FROM telco_customers LIMIT 10;
SELECT * FROM telco_customers LIMIT 1;

SELECT COUNT(*) FROM telco_customers;
SELECT churn, COUNT(*)
FROM telco_customers
GROUP BY churn;