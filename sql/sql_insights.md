# SQL INSIGHTS

## Key Findings Summary

**Geographic Performance Gaps (Query 1)**
The top customer areas by delivery time where delays are happening consitently, but this could still be by a multitude or reason. **What it does tell** us is that these **zones are worth studying** more in depth to consider rebalancing resources or adding coverage to reduce bottlenecks.

**Multi-Factor Performance Patterns (Query 2)**
Traffic combined with cuisine type and restaurant area shows how delays are shaped by context, not randomness. An important consideration is **if delivery time excludes prep, cuisine type has little effect**; if included, cuisines with longer prep times under heavy traffic create disproportionate delays. 

>Clarifying this definition is key for accurate operational planning.

**Performance Trend Detection (Query 5)**
*Month-to-month averages expose drivers with increasing delivery times*, an early signal of performance decline. While some rise is seasonal, individual outliers indicate where coaching, re-routing, or retraining may prevent customer dissatisfaction and delays in delivery.
>Month-to-month comparison chosen for Query 5 balances signal vs noise in fast-paced delivery operations. 
>
>Weekly analysis would capture too much variance from weather and traffic; quarterly would miss rapid performance changes in 
>high-turnover workforce.

---

## Business Implications

**Revenue Optimization**
The most profitable restaurant area (Query 4) may not align with operational efficiency. Understanding trade-offs between revenue and delivery delays enables smarter allocation of drivers and investment in high-demand areas.

**Employee Performance Management**
Monthly trend detection (Query 5) avoids daily noise and surfaces drivers whose efficiency is deteriorating. This allows interventions before delays affect customer satisfaction. The cadence is well-suited to a fast-paced business with high operational turnover.

**Operational Blind Spots**
Current queries emphasize revenue and time but leave out the *customer experience dimension*. Connecting delivery ratings to these metrics would clarify the boundaries within which profitability and satisfaction can be jointly maximized.

---
## Recommended Next Steps

**1. Driver Experience vs Performance Analysis**
   ```sql
    WITH driver_experience AS (
        SELECT 
            p.delivery_person_id,
            p.name,
            FLOOR(DATEDIFF('year', p.hired_date, d.order_placed_at)) AS years_experience,
            d.delivery_time_min
        FROM deliveries d
        JOIN delivery_persons p ON d.delivery_person_id = p.delivery_person_id
        WHERE p.is_active = TRUE
    )
    SELECT 
        years_experience,
        ROUND(AVG(delivery_time_min), 2) AS avg_delivery_time,
        COUNT(DISTINCT delivery_person_id) AS number_of_drivers
    FROM driver_experience
    GROUP BY years_experience
    ORDER BY years_experience;
   ```
   **Business Value**: Identifies if newer drivers systematically take longer and could be a possible cause of delays. This identifies whether onboarding processes need strengthening to target delays.


**2. Area-to-Area Delivery Performance Analysis**
   ```sql
    SELECT 
        d.restaurant_area,
        d.customer_area,
        ROUND(AVG(d.delivery_time_min), 2) AS avg_delivery_time,
        ROUND(AVG(d.delivery_distance_km), 2) AS avg_distance,
        ROUND(AVG(d.delivery_time_min) / AVG(d.delivery_distance_km), 2) AS time_per_km,
        COUNT(*) AS delivery_count,
        round(avg(delivery_rating),2) as avg_rating
    FROM deliveries d
    WHERE d.delivery_distance_km > 0
    GROUP BY d.restaurant_area, d.customer_area
    ORDER BY avg_delivery_time DESC
    LIMIT 20;
   ```
   **Business Value**: Surfaces underperforming origin–destination pairs where high delays persist even after adjusting for distance. These are the most likely candidates for routing, infrastructure, or resourcing issues.

3. **Economic Break-Even Analysis**
   ```sql
    WITH baseline AS (
        SELECT
            AVG(delivery_time_min) AS baseline_time,
            COUNT(*)               AS baseline_n
        FROM deliveries
        WHERE UPPER(TRIM(weather_condition)) = 'CLEAR'
        AND UPPER(TRIM(traffic_condition)) = 'LIGHT'
    ),
    condition_stats AS (
    SELECT
        UPPER(TRIM(weather_condition)) AS weather_condition,
        UPPER(TRIM(traffic_condition)) AS traffic_condition,
        AVG(delivery_time_min)         AS avg_delivery_time,
        AVG(delivery_rating)           AS avg_rating,
        COUNT(*)                       AS total_deliveries
    FROM deliveries
    WHERE weather_condition IS NOT NULL
    AND traffic_condition IS NOT NULL
    GROUP BY 1,2
    )
    SELECT
        cs.weather_condition,
        cs.traffic_condition,
        ROUND(cs.avg_delivery_time, 2)                AS avg_delivery_time,
        ROUND(b.baseline_time, 2)                     AS baseline_time,      
        ROUND(cs.avg_delivery_time - b.baseline_time, 2) AS additional_time, 
        ROUND(cs.avg_rating, 2)                       AS avg_rating,
        cs.total_deliveries
    FROM condition_stats cs
    CROSS JOIN baseline b
    WHERE NOT (cs.weather_condition = 'CLEAR' AND cs.traffic_condition = 'LIGHT')
    ORDER BY additional_time DESC;
   ```
   **Business Value**: This query compares delivery times and ratings across weather and traffic conditions against a **baseline of clear skies and light traffic** as our happy day scenario. It shows exactly how much extra time each scenario adds, helping pinpoint where delays are most severe. By highlighting these high-impact situations, operations teams can act with **targeted responses** like reallocating drivers, adjusting time estimates, or proactively updating customers.




