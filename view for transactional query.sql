--transactional views (real-time)
--complete transaction list
create or replace view vw_full_transactions as
select o.order_id, o.order_date, u.user_id, u.name as user_name,
	   c.course_id, c.course_name, od.price, od.final_price, v.voucher_code
from orders o 
join users u on o.user_id = u.user_id
join order_details od on o.order_id = od.order_id
join courses c on od.course_id = c.course_id
left join vouchers v on od.voucher_id = v.voucher_id;

select * from vw_full_transactions limit 100;

--details of participants who have completed the course
create or replace view vw_course_completions as 
select u.user_id, u.name, c.course_name, comp.completion_date
from completion comp
join order_details od on comp.order_detail_id = od.order_detail_id
join orders o on od.order_id = o.order_id
join users u on o.user_id = u.user_id 
join courses c on od.course_id = c.course_id 
where comp.completion_status = 'Completed';

select * from vw_course_completions vcc limit 100;

-- voucher usage details
create or replace view vw_voucher_usage_detail as 
select v.voucher_code, u.user_id, u.name, c.course_name, od.final_price, r.redemption_date
from vouchers v 
join redemption r on v.voucher_id = r.voucher_id
join order_details od on r.order_detail_id = od.order_detail_id
join orders o on od.order_id = o.order_id
join users u on o.user_id = u.user_id
join courses c on od.course_id = c.course_id;

select * from vw_voucher_usage_detail vvud limit 100;

-- list of participants per course
create or replace view vw_course_participants as 
select c.course_id, c.course_name, u.user_id, u.name as participant_name, od.enrollment_date
from courses c 
join order_details od on c.course_id = od.course_id
join orders o on od.order_id = o.order_id
join users u on o.user_id = u.user_id; 

select * from vw_course_participants vcp limit 100;

--user activity
create or replace view vw_user_activity as
select u.user_id, u.name, o.order_id, 
	   o.order_date, c.course_id, c.course_name, 
	   'purchase' as activity_type
from users u 
join orders o on u.user_id = o.user_id
join order_details od on o.order_id = od.order_id
join courses c on od.course_id = c.course_id 
union all 
select u.user_id, u.name,
	   null as order_id, 
	   comp.completion_date as activity_date,
	   c.course_id, c.course_name,
	   'course_completion' as activity_type
from users u
join orders o on u.user_id = o.user_id
join order_details od on o.order_id = od.order_id
join courses c on od.course_id = c.course_id
join completion comp on od.order_detail_id = comp.order_detail_id;

select * from vw_user_activity vua
where activity_type = 'purchase'
order by order_date asc
limit 20;