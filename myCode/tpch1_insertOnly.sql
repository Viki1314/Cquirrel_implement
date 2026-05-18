
use tpch1;

-- 【核心添加】临时关闭外键约束和唯一性检查，允许自由 delete 和导入
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;

TRUNCATE TABLE nation;
LOAD DATA INFILE '/mnt/e/projects/Cquirrel_implement/resource/tpch/1/nation.tbl'
INTO TABLE nation
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(n_nationkey, n_name, n_regionkey, n_comment, @dummy);

TRUNCATE TABLE customer;
LOAD DATA INFILE '/mnt/e/projects/Cquirrel_implement/resource/tpch/1/customer.tbl'
INTO TABLE customer
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment, @dummy);

TRUNCATE TABLE orders;
LOAD DATA INFILE '/mnt/e/projects/Cquirrel_implement/resource/tpch/1/orders.tbl'
INTO TABLE orders
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment, @dummy);

TRUNCATE TABLE lineitem;
LOAD DATA INFILE '/mnt/e/projects/Cquirrel_implement/resource/tpch/1/lineitem.tbl'
INTO TABLE lineitem
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(l_orderkey, l_partkey, l_suppkey, l_linenumber, l_quantity, l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment, @dummy);

-- 【核心添加】恢复环境安全设置
SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;

(
    select 'nation' as table_name, count(*) as row_count from nation
    union all
    select 'customer' as table_name, count(*) as row_count from customer
    union all
    select 'orders' as table_name, count(*) as row_count from orders
    union all
    select 'lineitem' as table_name, count(*) as row_count from lineitem
);