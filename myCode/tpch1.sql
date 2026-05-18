
use tpch1;

delete from nation;
LOAD DATA INFILE '/mnt/e/projects/Cquirrel_implement/resource/tpch/1/nation.tbl'
INTO TABLE nation
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(n_nationkey, n_name, n_regionkey, n_comment, @dummy);

delete from customer;
LOAD DATA INFILE '/mnt/e/projects/Cquirrel_implement/resource/tpch/1/customer.tbl'
INTO TABLE customer
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment, @dummy);

delete from orders;
LOAD DATA INFILE '/mnt/e/projects/Cquirrel_implement/resource/tpch/1/orders.tbl'
INTO TABLE orders
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment, @dummy);

delete from lineitem;
LOAD DATA INFILE '/mnt/e/projects/Cquirrel_implement/resource/tpch/1/lineitem.tbl'
INTO TABLE lineitem
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(l_orderkey, l_partkey, l_suppkey, l_linenumber, l_quantity, l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment, @dummy);

(
    select 'nation' as table_name, count(*) as row_count from nation
    union all
    select 'customer' as table_name, count(*) as row_count from customer
    union all
    select 'orders' as table_name, count(*) as row_count from orders
    union all
    select 'lineitem' as table_name, count(*) as row_count from lineitem
)