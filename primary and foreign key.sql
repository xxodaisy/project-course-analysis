--add primary key on the main table
alter table public.users 
add constraint pk_users primary key (user_id);

alter table public.courses 
add constraint pk_courses primary key (course_id);

alter table public.vouchers 
add constraint pk_vouchers primary key (voucher_id);

alter table public.orders 
add constraint pk_orders primary key (order_id);

alter table public.order_details 
add constraint pk_order_details primary key (order_detail_id);

alter table public.redemption 
add constraint pk_redemption primary key (redemption_id);

alter table public.completion 
add constraint pk_completion primary key (completion_id);

-- add foreign key
-- Relation order_details → orders
ALTER TABLE public.order_details 
ADD CONSTRAINT fk_order_details_order
FOREIGN KEY (order_id) REFERENCES public.orders(order_id);

-- Relation order_details → courses
ALTER TABLE public.order_details 
ADD CONSTRAINT fk_order_details_course
FOREIGN KEY (course_id) REFERENCES public.courses(course_id);

-- Relation order_details → vouchers
ALTER TABLE public.order_details 
ADD CONSTRAINT fk_order_details_voucher
FOREIGN KEY (voucher_id) REFERENCES public.vouchers(voucher_id);

-- Relation orders → users
alter table public.orders
add constraint fk_orders_user
foreign key (user_id) references public.users(user_id);

-- Relation vouchers → users
alter table public.vouchers
add constraint fk_vouchers_user
foreign key (user_id) references public.users(user_id);

-- Relation redemption → order_details
alter table public.redemption 
add constraint fk_redemption_order_detail
foreign key (order_detail_id) references public.order_details (order_detail_id);

-- Relation redemption → vouchers
alter table public.redemption 
add constraint fk_redemption_vouchers
foreign key (voucher_id) references public.vouchers (voucher_id);

-- Relation completion → order_details
alter table public.completion
add constraint fk_completion_order_detail
foreign key (order_detail_id) references public.order_details (order_detail_id);