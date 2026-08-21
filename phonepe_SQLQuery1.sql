use phonepe;
CREATE TABLE aggregated_insurance (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Insurance_type VARCHAR(50),
    Insurance_count BIGINT,
    Insurance_amount BIGINT
);
GO
SELECT TOP 10 * 
FROM aggregated_insurance;
CREATE TABLE aggregated_transaction (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Transaction_type VARCHAR(50),
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);
GO

CREATE TABLE aggregated_user (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Brands VARCHAR(50),
    Transaction_count BIGINT,
    Percentage FLOAT
);
GO
# map
CREATE TABLE map_insurance (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Districts VARCHAR(100),
    Transaction_count BIGINT,
    Transaction_amount FLOAT
);
GO
CREATE TABLE map_transaction (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    District VARCHAR(100),
    Transaction_count BIGINT,
    Transaction_amount FLOAT
);
CREATE TABLE map_user (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Districts VARCHAR(100),
    RegisteredUser BIGINT,
    AppOpens BIGINT
);
CREATE TABLE top_insurance (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Pincodes VARCHAR(20),
    Transaction_count BIGINT,
    Transaction_amount FLOAT
);
CREATE TABLE top_transaction (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Pincodes VARCHAR(20),
    Transaction_count BIGINT,
    Transaction_amount FLOAT
);
CREATE TABLE top_user (
    States VARCHAR(50),
    Years INT,
    Quarter INT,
    Pincodes VARCHAR(20),
    RegisteredUser BIGINT
);
SELECT name
FROM sys.tables;
SELECT TOP 10 * 
FROM aggregated_user;


--case study
--Business Case 1 
---Decoding Transaction Dynamics on PhonePe--
-– Query 1.
SELECT
    Transaction_type,
    SUM(Transaction_count) AS Total_Transactions,
    SUM(Transaction_amount) AS Total_Amount
FROM aggregated_transaction
GROUP BY Transaction_type
ORDER BY Total_Amount DESC;
--Query 2 — State-wise Transaction Performance
SELECT TOP 10
    States,
    SUM(Transaction_amount) AS Total_Amount
FROM aggregated_transaction
GROUP BY States
ORDER BY Total_Amount DESC;
--Query 3 — Year-wise Transaction Growth
SELECT
    Years,
    SUM(Transaction_count) AS Total_Transactions,
    SUM(Transaction_amount) AS Total_Amount
FROM aggregated_transaction
GROUP BY Years
ORDER BY Years;