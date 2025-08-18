--buat index
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_order_details_order_id ON order_details(order_id);
CREATE INDEX idx_order_details_course_id ON order_details(course_id);
CREATE INDEX idx_order_details_voucher_id ON order_details(voucher_id);
CREATE INDEX idx_redemption_order_detail_id ON redemption(order_detail_id);
CREATE INDEX idx_completion_order_detail_id ON completion(order_detail_id);


--buat materialized view 
--create materialized view mv_full_transactions as
--SELECT
--    u.user_id,
--    u.gender,
--    u.age,
--    u.education,
--    u.occupation,
--    u.region,
--    c.course_id,
--    c.course_name,
--    c.category,
--    od.price AS original_price,
--    od.discount_percent,
--    od.final_price,
--    r.redemption_status,
--    r.redemption_date,
--    comp.completion_status,
--    comp.completion_date,
--    o.order_date,
--    od.enrollment_date
--FROM order_details od
--LEFT JOIN courses c ON od.course_id = c.course_id
--LEFT JOIN vouchers v ON od.voucher_id = v.voucher_id
--LEFT JOIN redemption r ON od.order_detail_id = r.order_detail_id
--LEFT JOIN completion comp ON od.order_detail_id = r.order_detail_id
--LEFT JOIN orders o on od.order_id = o.order_id
--LEFT JOIN users u ON o.user_id = u.user_id;
--WHERE o.order_date >= CURRENT_DATE - interval '6 months';
--
--REFRESH MATERIALIZED VIEW mv_full_transactions;
