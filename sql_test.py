import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DESKTOP-55JNORK\\SQLEXPRESS;"
    "DATABASE=phonepe;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

print("SQL Connected Successfully!")