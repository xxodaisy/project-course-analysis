--analytical query materalized view
-- materialized view courses_sales
create materialized view mv_course_sales as
select c.course_id, c.course_name,
	   DATE_TRUNC('month', o.order_date) as month,
	   count(od.order_detail_id) as total_sold,
	   sum(od.final_price) as total_revenue
from courses c
join order_details od on c.course_id = od.course_id
join orders o on od.order_id = o.order_id
group by c.course_id, c.course_name, DATE_TRUNC('month', o.order_date);

select * from mv_course_sales mcs limit 100;

-- materialized view voucher_usage for voucher performance (how many times the voucher has been used, total discount)
create materialized view mv_voucher_usage as 
select v.voucher_code,
	   count(r.redemption_id) as usage_count,
	   sum(od.price - od.final_price) as total_discount,
	   min(r.redemption_date) as first_used,
	   max(r.redemption_date) as last_used
from vouchers v
left join redemption r on v.voucher_id = r.voucher_id
left join order_details od on r.order_detail_id = od.order_detail_id
group by v.voucher_code;

select * from mv_voucher_usage mvu limit 100;

-- materialized view course_completion_rate
drop materialized view mv_course_completion_rate;

CREATE MATERIALIZED VIEW mv_course_completion_rate AS
SELECT c.course_id, c.course_name,
       COUNT(comp.completion_id) AS completed_count,
       COUNT(od.order_detail_id) AS total_enrolled,
       ROUND(COUNT(comp.completion_id)::NUMERIC / NULLIF(COUNT(od.order_detail_id), 0) * 100, 2) AS completion_rate
FROM courses c
JOIN order_details od ON c.course_id = od.course_id
LEFT JOIN completion comp ON od.order_detail_id = comp.order_detail_id
GROUP BY c.course_id, c.course_name;

refresh materialized view mv_course_completion_rate;

select * from mv_course_completion_rate mccr;

--buat mv top users
create materialized view mv_top_users as 
select u.user_id, u.name,
	   sum(od.final_price) as total_spent,
	   count(distinct o.order_id) as total_orders
from users u 
join orders o on u.user_id = o.user_id
join order_details od on o.order_id = od.order_id
group by u.user_id, u.name
order by total_spent desc;

select * from mv_top_users mtu limit 10;