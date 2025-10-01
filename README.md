# Course Analysis – E-Learning Platform

## Project Overview
This project simulates a specialized online platform that allows users to purchase courses with or without discount vouchers, redeem vouchers, enroll in classes, and complete classes.

The database is designed to support transaction analysis (operational) and business analysis (strategic) to understand course performance, discount effectiveness, users behavior, and revenue growth potential.

## Goals
- Transactional: providing details information about transaction, redeem voucher, enrollment, and user’s completion.
  
- Analytical: generating insights about courses completion, discount effectiveness, sales trend, and users behavior to supporting strategic decisions.
  
- Monitoring: calculating important metric, such as revenue, growth rate, and engagement to evaluation the platform.

## Tools
- PostgreSQL → database storage and query execution.
  
- Python → creation of dummy datasets and data validation.
  
- DBeaver → database management and query builder.
  
- Metabase → dashboard visualization and data exploration.

## Datasets
### Parameter

NUM_USERS = 10_000

NUM_VOUCHERS = 50_000

NUM_ORDERS = 30_000

TARGET_TX = 80_000

VOUCHER_USAGE_RATE = 0.6

COURSES_PER_ORDER = (1,3)

Determining the amount of data for each table and its behavior, consisting of:
- **Total users**: 10.000
- **Vouchers**: 50.000
- **Orders**: 30.000
- **Transaction** target: 80.000
- 60% of order use voucher
Each order have 1–3 courses, some use vouchers and not use vouchers.

### Entities
- **users**: participant data.
- **courses**: courses on sale.
- **vouchers**: voucher and discount (valid period and discount amount).
- **orders**: courses purchase (with or without voucher).
- **order details**: details of each item (courses) purchased in a single order.
- **redemption**: voucher and status of redeem.
- **completion**: status of completion class.

### Data Structures
- **users**: user_id, user_name, name, age, gender, email,phone_number, occupation, region, education, major
- **courses**: course_id, course_name, category,price, duration_days
- **vouchers**: voucher_id, user_id, voucher_code, discount_percent, status, start_date, end_date.
- **orders**: order_id, user_id, order_date, status, total_price, payment_method
- **order_details**: order_detail_id, order_id, course_id, voucher_id, price, discount_percent, final_price, enrollment_date
- **redemption**: redemption_id, order_detail_id, voucher_id, redemption_date, redemption_status
- **completion**: completion_id, order_detail_id, completion_status, completion_date

## Analysis Steps
- Data Preparation
Exploring the data (create a transactional and analytical queries — also get insights and recommendation from the data)
Create a dashboard interactive (using Metabase)

The following steps will be taken to data preparation:
- Designing the database
- Generate dummy data (using Python)
- Load to DBeaver
- Cleansing data

## Dashboards
- Transaction summary → A consolidated view of all recent transactions, including key metrics such as total users, revenue, active paying users, and average revenue per user.
  
- Voucher usage tracking → Detailed monitoring of voucher redemption, highlighting usage trends, most active users, and the impact of vouchers across different courses.
  
- Course participations → An overview of course enrollments and completions, showcasing participant distribution per course, category performance, and learning engagement trends.
  
- Analytical Overviews → a high-level summary of key business metrics and trends, providing a quick snapshot of overall platform performance.
  
- User Demographics & Engagement → insights into user characteristics (e.g., age, location, type of users) and their engagement patterns, such as activity levels, retention, and interaction with courses.
  
- Revenue & Sales → Analysis of financial performance, including total revenue, sales growth, conversion rates, and average order values across different time periods.
  
- Course Performance & Sales → Evaluation of course popularity and effectiveness, covering enrollment numbers, completion rates, top-performing courses, and revenue contribution by category.
  
- Voucher & Discount Insights → Tracking the usage and impact of vouchers and discounts, including redemption trends, top users of vouchers, and their influence on overall sales and customer behavior.

## Full Project
- Creating a dummy data → [Building a Realistic E-Learning Dataset: From Dummy Data to Database](https://medium.com/@fleursansvoix/building-a-realistic-e-learning-dataset-from-dummy-data-to-database-510506b408e8)
  
- Part 1 → [Turning Dummy Data into Business Insights: An E-Learning Analysis Case Study Part 1](https://medium.com/@fleursansvoix/turning-dummy-data-into-business-insights-an-e-learning-analytics-case-study-part-1-a2d2d520506c)
  
- Part 2 → [Turning Dummy Data into Business Insights: An E-Learning Analysis Case Study Part 2](https://medium.com/@fleursansvoix/turning-dummy-data-into-business-insights-an-e-learning-analysis-case-study-part-2-7555f371997e)
