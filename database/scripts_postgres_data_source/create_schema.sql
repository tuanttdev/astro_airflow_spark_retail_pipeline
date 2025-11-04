-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- DROP SEQUENCE public.channels_channel_id_seq;

CREATE SEQUENCE public.channels_channel_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.channels_channel_id_seq1;

CREATE SEQUENCE public.channels_channel_id_seq1
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.channel_targets definition

-- Drop table

-- DROP TABLE public.channel_targets;

CREATE TABLE public.channel_targets (
	target_id text NOT NULL,
	"month" text NULL,
	"year" int4 NULL,
	channel text NULL,
	target_revenue numeric(18, 2) NULL,
	target_orders int4 NULL,
	target_conversion_rate numeric(6, 4) NULL,
	target_avg_order numeric(18, 2) NULL,
	target_roi numeric(6, 2) NULL,
	created_at timestamptz DEFAULT now() NULL,
	updated_at timestamptz DEFAULT now() NULL,
	CONSTRAINT channel_targets_pkey PRIMARY KEY (target_id)
);


-- public.channels definition

-- Drop table

-- DROP TABLE public.channels;

CREATE TABLE public.channels (
	channel_name text NOT NULL,
	"type" text NULL,
	commission_rate numeric(6, 4) NULL,
	monthly_fixed_cost numeric(18, 2) NULL,
	avg_acquisition_cost numeric(18, 2) NULL,
	created_at timestamptz DEFAULT now() NULL,
	updated_at timestamptz DEFAULT now() NULL,
	channel_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	CONSTRAINT channels_pkey PRIMARY KEY (channel_name)
);


-- public.customers definition

-- Drop table

-- DROP TABLE public.customers;

CREATE TABLE public.customers (
	customer_id text NOT NULL,
	"name" text NULL,
	email text NULL,
	phone text NULL,
	city text NULL,
	registration_date date NULL,
	segment text NULL,
	lifetime_value numeric(18, 2) NULL,
	total_orders int4 NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL,
	CONSTRAINT customers_pkey PRIMARY KEY (customer_id)
);


-- public.employee_targets definition

-- Drop table

-- DROP TABLE public.employee_targets;

CREATE TABLE public.employee_targets (
	target_id text NOT NULL,
	"month" text NULL,
	"year" int4 NULL,
	employee_id text NULL,
	store_id text NULL,
	team_id text NULL,
	primary_channel text NULL,
	target_revenue numeric(18, 2) NULL,
	target_orders int4 NULL,
	target_conversion_rate numeric(6, 4) NULL,
	target_avg_transaction numeric(18, 2) NULL,
	target_upsell_rate numeric(6, 4) NULL,
	created_at timestamptz DEFAULT now() NULL,
	updated_at timestamptz DEFAULT now() NULL,
	CONSTRAINT employee_targets_pkey PRIMARY KEY (target_id)
);


-- public.employees definition

-- Drop table

-- DROP TABLE public.employees;

CREATE TABLE public.employees (
	employee_id text NOT NULL,
	"name" text NULL,
	store_id text NULL,
	team_id text NULL,
	"position" text NULL,
	hire_date date NULL,
	base_salary numeric(18, 2) NULL,
	commission_rate numeric(6, 4) NULL,
	performance_rating text NULL,
	created_at timestamptz DEFAULT now() NULL,
	updated_at timestamptz DEFAULT now() NULL,
	CONSTRAINT employees_pkey PRIMARY KEY (employee_id)
);


-- public.order_items definition

-- Drop table

-- DROP TABLE public.order_items;

CREATE TABLE public.order_items (
	item_id text NOT NULL,
	order_id text NULL,
	product_id text NULL,
	quantity int4 NULL,
	unit_price numeric(18, 2) NULL,
	subtotal numeric(18, 2) NULL,
	discount numeric(18, 2) NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL
);


-- public.orders definition

-- Drop table

-- DROP TABLE public.orders;

CREATE TABLE public.orders (
	order_id text NOT NULL,
	order_date date NULL,
	customer_id text NULL,
	store_id text NULL,
	employee_id text NULL,
	channel text NULL,
	total_amount numeric(18, 2) NULL,
	discount_amount numeric(18, 2) NULL,
	final_amount numeric(18, 2) NULL,
	payment_method text NULL,
	status text NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL,
	CONSTRAINT orders_pkey PRIMARY KEY (order_id)
);


-- public.products definition

-- Drop table

-- DROP TABLE public.products;

CREATE TABLE public.products (
	product_id text NOT NULL,
	"name" text NULL,
	category text NULL,
	brand text NULL,
	cost_price numeric(18, 2) NULL,
	selling_price numeric(18, 2) NULL,
	stock int4 NULL,
	supplier text NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL,
	status varchar NULL,
	CONSTRAINT products_pkey PRIMARY KEY (product_id)
);


-- public.store_targets definition

-- Drop table

-- DROP TABLE public.store_targets;

CREATE TABLE public.store_targets (
	target_id text NOT NULL,
	"month" text NULL,
	"year" int4 NULL,
	store_id text NULL,
	target_revenue numeric(18, 2) NULL,
	target_orders int4 NULL,
	target_conversion_rate numeric(6, 4) NULL,
	target_avg_order numeric(18, 2) NULL,
	target_customer_satisfaction numeric(3, 1) NULL,
	created_at timestamptz DEFAULT now() NULL,
	updated_at timestamptz DEFAULT now() NULL,
	CONSTRAINT store_targets_pkey PRIMARY KEY (target_id)
);


-- public.stores definition

-- Drop table

-- DROP TABLE public.stores;

CREATE TABLE public.stores (
	store_id text NOT NULL,
	"name" text NULL,
	city text NULL,
	region text NULL,
	"type" text NULL,
	opening_date date NULL,
	area_sqm int4 NULL,
	monthly_rent numeric(18, 2) NULL,
	manager text NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL,
	CONSTRAINT stores_pkey PRIMARY KEY (store_id)
);


-- public.team_targets definition

-- Drop table

-- DROP TABLE public.team_targets;

CREATE TABLE public.team_targets (
	target_id text NOT NULL,
	"month" text NULL,
	"year" int4 NULL,
	team_id text NULL,
	store_id text NULL,
	target_revenue numeric(18, 2) NULL,
	target_orders int4 NULL,
	target_conversion_rate numeric(6, 4) NULL,
	target_team_productivity numeric(18, 2) NULL,
	created_at timestamptz DEFAULT now() NULL,
	updated_at timestamptz DEFAULT now() NULL,
	CONSTRAINT team_targets_pkey PRIMARY KEY (target_id)
);


-- public.teams definition

-- Drop table

-- DROP TABLE public.teams;

CREATE TABLE public.teams (
	team_id text NOT NULL,
	team_name text NULL,
	store_id text NULL,
	team_leader text NULL,
	member_count int4 NULL,
	created_at timestamptz NULL,
	updated_at timestamptz NULL,
	CONSTRAINT teams_pkey PRIMARY KEY (team_id)
);