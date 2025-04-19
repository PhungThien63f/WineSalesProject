---1.Total Bottles Sold per Year: Calculate the total number of bottles sold each year from 2017 to 2023.
select extract(year from date) as year, sum(bottles_sold) as total_bottles_sold
from sales_data.sales
where bottles_sold > 0 
group by 1
order by 1

--- 2.Top 3 Vendors per City: Identify the top three vendors (Vendor Name) with the highest sales (by bottle count) in each city.
with ranked_vendors as (
    select city_name, vendor_name, sum(bottles_sold) as total_bottles_sold,
        row_number() over (partition by city_name order by sum(bottles_sold) desc) as rank
    from sales_data.sales as s
    left join sales_data.vendor_dim as v
        on s.vendor_id = v.vendor_id
	WHERE bottles_sold > 0
    GROUP BY 1,2
)

select city_name, vendor_name, total_bottles_sold,rank
from ranked_vendors
where rank <= 3

-- 3.Sales Analysis by Category: Analyze the sales trends for the top-selling wine categories (Category Name) year by year.
-- top 3
with top_3_cat as (
select category_name, sum(bottles_sold) as total_bottles_sold
from sales_data.sales as sales 
left join sales_data.category_dim as cat 
on sales.category_id = cat.category_id 
where bottles_sold > 0 
group by 1 
order by 1 desc 
limit 3
)

select category_name, EXTRACT(YEAR FROM date) AS year, sum(bottles_sold) as total_bottles_sold
from sales_data.sales as sales left join 
sales_data.category_dim as cat
on sales.category_id = cat.category_id 
where category_name in (select category_name
						from top_3_cat)
group by 1,2 
order by 1,2 


-- 4.Top Stores by Sales per City: Identify the stores (Store Name) with the highest wine sales in each city in the most recent year (2023).
with stores_rank as (
select store_name, city_name, sum(bottles_sold) as total_bottles_sold,
row_number() over(partition by city_name order by sum(bottles_sold) desc) as rank
from sales_data.sales as s 
left join sales_data.store_dim as st
on s.store_id = st.store_id 
where bottles_sold > 0 and EXTRACT(YEAR FROM date) = 2023 
group by 1, 2
order by 1, 2
)

select store_name, city_name, total_bottles_sold 
from stores_rank 
where rank = 1



-- 5.Vendor Sales Share: Calculate the percentage of total sales for each vendor (Vendor Name) compared to the overall sales of all vendors across the entire time period (2017-2023).
with vendor_sales as (
select vendor_name, sum(bottles_sold) as total_bottles_sold 
from sales_data.sales as s
left join sales_data.vendor_dim as v
on s.vendor_id = v.vendor_id 
where bottles_sold > 0
group by 1
), 

total_sales as 
(select sum(total_bottles_sold) as overall_bottles_sold
from vendor_sales
)
select v.vendor_name, v.total_bottles_sold, ROUND((v.total_bottles_sold * 100.0) / t.overall_bottles_sold , 2) AS sales_share_percentage
FROM vendor_sales v, total_sales t
ORDER BY sales_share_percentage desc