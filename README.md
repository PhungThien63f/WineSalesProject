# 🍷 Wine Sales Analysis Dashboard (2017–2023)

## 📌 Overview
This project focuses on analyzing wine sales data from 2017 to 2023. It includes data processing, schema design using a star schema, SQL-based data exploration, and dashboard creation with Power BI to uncover business insights across stores, vendors, and product categories.


## Overview Processing 

![Dashboard Preview](https://github.com/PhungThien63f/WineSalesProject/blob/main/Intro.png)

## 🧩 Project Components

### 1. **Data Management**
- Designed a **Star Schema** with one fact table (`sales`) and multiple dimension tables (`store_dim`, `vendor_dim`, `category_dim`, etc.).
- Resolved data inconsistencies:
- Store name normalization.
- Differentiation between vendor city and store city.

### 2. **SQL Analytics**
Executed multiple SQL queries to generate insights:

- 📅 **Total Bottles Sold per Year**
  
```sql
SELECT 
    EXTRACT(YEAR FROM date) AS year,
    SUM(bottles_sold) AS total_bottles_sold
FROM 
    sales_data.sales
WHERE 
    bottles_sold > 0
GROUP BY 
    1
ORDER BY 
    1;
```

    
- 🏙️ **Top 3 Vendors per City**  
- 🍾 **Sales Trend by Wine Category**  
- 🏬 **Top Stores by Sales (2023)**  
- 📊 **Vendor Sales Share**

### 3. **Power BI Dashboard**
A dynamic dashboard was created to visualize:
- Sales trends over years.
- Top-performing vendors and stores.
- Category breakdown and vendor market share.

![Category Breakdown](https://github.com/PhungThien63f/WineSalesProject/blob/main/dashboard.png)

## 📈 Business Insights
- Identified key vendors and store performance by city.
- Highlighted seasonal patterns and long-term growth.
- Showed relative performance of vendors across regions.

## 🛠️ Tools & Technologies
- **SQL** (PostgreSQL)
- **Power BI**
- **Star Schema Design**
- **Data Cleaning & Normalization**

