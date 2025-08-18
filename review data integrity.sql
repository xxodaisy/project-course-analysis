--there cannot be order_details without an order
select od.*
from order_details od
left join orders o on od.order_id = o.order_id 
where o.order_id is null;

-- there cannot be completion without order_details
select c.*
from completion c 
left join order_details od on c.order_detail_id = od.order_detail_id 
where od.order_detail_id is null;

-- time integrity check
select *
from redemption r 
join order_details od on r.order_detail_id = od.order_detail_id 
join orders o on od.order_id = o.order_id
where r.redemption_date  < o.order_date; 

-- time integrity check
select * 
from order_details od 
join orders o on od.order_id = o.order_id
where od.enrollment_date < o.order_date;

-- time integrity check
select * 
from order_details od 
join orders o on od.order_id = o.order_id
join completion c on od.order_detail_id  = c.order_detail_id 
where c.completion_date < od.enrollment_date; 

select * from vouchers;

-- vouchers that have expired but can still be used, with the status redeem = Expired
select o.order_id, o.order_date, v.voucher_code, v.discount_percent, v.status, c.completion_status,
	   (current_date - interval '12 month') as start_date_voucher,
	   (current_date - interval '6 month') as expiry_date_voucher
from orders o
left join order_details od on o.order_id = od.order_id
left join vouchers v on od.voucher_id = v.voucher_id
left join completion c on od.order_detail_id = c.order_detail_id
left join redemption r on od.order_detail_id = r.order_detail_id 
where r.redemption_status = 'Expired';



