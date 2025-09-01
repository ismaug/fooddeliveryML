/* -------------------------------------------------------------------
   File: sql_queries.sql
   Project: Data scientist internship technical assessment
   Author: Rafaela Black
   Date: [YYYY-MM-DD]
   -------------------------------------------------------------------
   Description:
   This file contains SQL queries designed to answer the business
   questions outlined in the assessment.
------------------------------------------------------------------- */

/* ================================================================
   1. Top 5 customer areas with highest average delivery time
      in the last 30 days
================================================================ */
SELECT customer_area,
       round(Avg(delivery_time_min),2) AS avg_delivery_time
FROM   deliveries
WHERE  order_placed_at >= CURRENT_DATE - INTERVAL '30 day'
GROUP  BY customer_area
ORDER  BY avg_delivery_time DESC
LIMIT  5;


/* ================================================================
   2. Average delivery time per traffic condition,
      by restaurant area and cuisine type
================================================================ */
SELECT
    r.area AS restaurant_area,
    r.cuisine_type,
    d.traffic_condition,
    Avg(d.delivery_time_min) AS avg_delivery_time
FROM deliveries d
JOIN orders o ON d.delivery_id = o.delivery_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE d.traffic_condition IS NOT NULL
GROUP BY d.traffic_condition, r.area, r.cuisine_type
ORDER BY d.traffic_condition, r.area, r.cuisine_type;

/* ================================================================
   3. Top 10 delivery people with the fastest average delivery time
      (at least 50 deliveries and still active)
================================================================ */
SELECT p.name, Round(Avg(delivery_time_min), 2) AS avg_delivery_time, Count(*) AS total_deliveries
FROM deliveries d
JOIN delivery_persons p
ON d.delivery_person_id = p.delivery_person_id
WHERE p.is_active = true
GROUP BY p.delivery_person_id, p.name
HAVING COUNT(*) >= 50
ORDER BY avg_delivery_time
LIMIT 10


/* ================================================================
   4. Most profitable restaurant area in the last 3 months
      (highest total order value)
================================================================ */
SELECT Sum(order_value) AS total_revenue, r.area, Count(DISTINCT o.order_id) AS total_orders
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN deliveries d ON o.delivery_id = d.delivery_id
WHERE d.order_placed_at >= CURRENT_DATE - INTERVAL '3 month'
GROUP BY r.area
ORDER BY total_revenue DESC
LIMIT 1


/* ================================================================
   5. Delivery people with increasing trend in average delivery time
================================================================ */
WITH monthly_average AS (SELECT
    p.delivery_person_id,
    p.name,
    round(avg(d.delivery_time_min),2) AS avg_delivery_time,
    date_trunc('Month', d.order_placed_at) AS month_year
  FROM deliveries d
  JOIN delivery_persons p
  ON d.delivery_person_id = p.delivery_person_id
  WHERE p.hired_date <= date_trunc('month', CURRENT_DATE) - INTERVAL '2 MONTH'
  GROUP BY p.delivery_person_id, p.name, date_trunc('Month', d.order_placed_at)
  HAVING date_trunc('Month', d.order_placed_at) >=  CURRENT_DATE - INTERVAL '2 MONTH'
  ORDER BY p.delivery_person_id, month_year
 ),
  with_lag AS (SELECT *, lag(avg_delivery_time, 1)
    over (partition BY delivery_person_id
    ORDER BY month_year) AS prev_avg_delivery_time,
    avg_delivery_time - prev_avg_delivery_time AS difference
    FROM monthly_average)
SELECT delivery_person_id, name, avg_delivery_time, prev_avg_delivery_time, difference AS increase
FROM with_lag
WHERE prev_avg_delivery_time IS NOT NULL AND difference > 0;

/* ================================================================
   End of SQL queries