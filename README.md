# Construction Equipment Division Performance Dashboard

An end-to-end data analytics project analyzing equipment sales and performance trends across multiple construction equipment divisions (Earthmoving, Material Handling, Excavators, Mini Excavators), built using **Power BI, Python, and SQL**.

> Note: This project uses public/sample data and is built independently to demonstrate dashboarding, ETL, and data modeling skills. It is not affiliated with or built using any confidential client data.

## Project Overview

This dashboard helps track division-wise sales performance, profitability, and regional trends for a construction equipment business. It simulates a real-world business intelligence workflow: raw data → cleaning/transformation → SQL analysis → Power BI visualization.

## Tools Used

- **Power BI**: Star Schema data modeling, DAX measures, drill-through reports, slicers
- **Python (Pandas, NumPy)**: Data cleaning, transformation, feature engineering, validation
- **SQL (MySQL/PostgreSQL)**: Joins, CTEs, Window Functions, Views for data consolidation and analysis
- **Apache Airflow**: DAG-based orchestration of the daily ETL pipeline (extract → clean → load → quality check → Power BI refresh)

## Folder Structure

```
construction-equipment-dashboard/
├── README.md
├── data/
│   ├── equipment_sales_sample.csv      # raw sample data
│   ├── equipment_sales_cleaned.csv     # output of data_cleaning.py
│   └── division_summary.csv            # output of data_cleaning.py
├── python/
│   └── data_cleaning.py                # cleaning & transformation script
├── sql/
│   └── queries.sql                     # analysis queries & view
├── airflow/
│   └── dags/
│       └── equipment_sales_pipeline_dag.py   # Airflow DAG orchestrating the pipeline
├── powerbi/
│   └── dashboard.pbix                  # Power BI dashboard file
└── screenshots/
    └── dashboard_preview.png
```

## Key Features

- Division-wise KPI cards (units sold, revenue, profit, margin %)
- Region and time-period slicers for interactive filtering
- Drill-through reports from division summary to dealer-level detail
- Month-over-month revenue trend analysis
- Top-performing dealer ranking per division
- Daily automated ETL pipeline orchestrated with Apache Airflow (extract → clean → load → quality checks → Power BI refresh)

## How to Run

1. Clone this repository.
2. Run `python python/data_cleaning.py` to generate cleaned datasets.
3. (Optional) Load `sql/queries.sql` into MySQL/PostgreSQL to recreate the analysis tables and views.
4. Open `powerbi/dashboard.pbix` in Power BI Desktop and refresh the data source to point to the cleaned CSVs.

## Author

**Harshad Gandhale**
Data Analyst | Power BI | SQL | Python | Business Intelligence
[LinkedIn](https://www.linkedin.com/in/harshad-gandhale-68a678218) | [GitHub](https://github.com/harshadgandhalegit-dot)
