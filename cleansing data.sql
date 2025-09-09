--deteksi duplikat user_id
select user_id, count(*)
from users u
group by u.user_id 
having count(*) > 1;

--deteksi duplikat course_id
select course_id, count(*)
from courses c 
group by c.course_id
having count(*) > 1;

--deteksi duplikat voucher_id
select voucher_id, count(*)
from vouchers v 
group by v.voucher_id  
having count(*) > 1;

--deteksi duplikat order_id
select order_id, count(*)
from orders o 
group by o.order_id
having count(*) > 1;

--deteksi duplikat order_detail_id
select order_detail_id, count(*)
from order_details od 
group by od.order_detail_id
having count(*) > 1;


--deteksi duplikat redemption_id
select redemption_id, count(*)
from redemption r
group by r.redemption_id
having count(*) > 1;

--deteksi duplikat completion_id
select completion_id, count(*)
from completion comp 
group by comp.completion_id
having count(*) > 1;

--deteksi outlier
select * 
from order_details od
where od.price <= 0;

select *
from order_details od
where od.final_price <= 0;

select *
from courses c 
where c.price <= 0;

--cek missing value
select *
from order_details od 
join orders o on od.order_id = o.order_id
where o.order_date is null or od.final_price is null; 

--cek integritas waktu
select *
from redemption r 
join order_details od on r.order_detail_id = od.order_detail_id 
join orders o on od.order_id = o.order_id
where r.redemption_date  < o.order_date;

select * 
from order_details od 
join orders o on od.order_id = o.order_id
where od.enrollment_date < o.order_date;

select * 
from order_details od 
join orders o on od.order_id = o.order_id
join completion c on od.order_detail_id  = c.order_detail_id 
where c.completion_date < od.enrollment_date;


