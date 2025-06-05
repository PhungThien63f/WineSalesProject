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
```sql
  WITH ranked_vendors AS (
    SELECT 
        city_name, 
        vendor_name, 
        SUM(bottles_sold) AS total_bottles_sold,
        ROW_NUMBER() OVER (PARTITION BY city_name ORDER BY SUM(bottles_sold) DESC) AS rank
    FROM 
        sales_data.sales AS s
    LEFT JOIN 
        sales_data.vendor_dim AS v ON s.vendor_id = v.vendor_id
    WHERE 
        bottles_sold > 0
    GROUP BY 
        city_name, vendor_name
)
SELECT 
    city_name, 
    vendor_name, 
    total_bottles_sold,
    rank
FROM 
    ranked_vendors
WHERE 
    rank <= 3;
```

- 🍾 **Sales Trend by Wine Category**
```sql 
  WITH top_3_cat AS (
    SELECT 
        category_name, 
        SUM(bottles_sold) AS total_bottles_sold
    FROM 
        sales_data.sales AS sales
    LEFT JOIN 
        sales_data.category_dim AS cat ON sales.category_id = cat.category_id
    WHERE 
        bottles_sold > 0
    GROUP BY 
        category_name
    ORDER BY 
        total_bottles_sold DESC
    LIMIT 3
)
SELECT 
    category_name, 
    EXTRACT(YEAR FROM date) AS year, 
    SUM(bottles_sold) AS total_bottles_sold
FROM 
    sales_data.sales AS sales
LEFT JOIN 
    sales_data.category_dim AS cat ON sales.category_id = cat.category_id
WHERE 
    category_name IN (SELECT category_name FROM top_3_cat)
GROUP BY 
    category_name, year
ORDER BY 
    category_name, year;
```
- 🏬 **Top Stores by Sales (2023)**
``` sql 
  WITH stores_rank AS (
    SELECT 
        store_name, 
        city_name, 
        SUM(bottles_sold) AS total_bottles_sold,
        ROW_NUMBER() OVER (PARTITION BY city_name ORDER BY SUM(bottles_sold) DESC) AS rank
    FROM 
        sales_data.sales AS s
    LEFT JOIN 
        sales_data.store_dim AS st ON s.store_id = st.store_id
    WHERE 
        bottles_sold > 0 
        AND EXTRACT(YEAR FROM date) = 2023
    GROUP BY 
        store_name, city_name
)
SELECT 
    store_name, 
    city_name, 
    total_bottles_sold
FROM 
    stores_rank
WHERE 
    rank = 1;
```
- 📊 **Vendor Sales Share**
  
```sql 
  WITH vendor_sales AS (
    SELECT 
        vendor_name, 
        SUM(bottles_sold) AS total_bottles_sold
    FROM 
        sales_data.sales AS s
    LEFT JOIN 
        sales_data.vendor_dim AS v ON s.vendor_id = v.vendor_id
    WHERE 
        bottles_sold > 0
    GROUP BY 
        vendor_name
), 
total_sales AS (
    SELECT 
        SUM(total_bottles_sold) AS overall_bottles_sold
    FROM 
        vendor_sales
)
SELECT 
    v.vendor_name, 
    v.total_bottles_sold, 
    ROUND((v.total_bottles_sold * 100.0) / t.overall_bottles_sold, 2) AS sales_share_percentage
FROM 
    vendor_sales v, 
    total_sales t
ORDER BY 
    sales_share_percentage DESC;
```

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

