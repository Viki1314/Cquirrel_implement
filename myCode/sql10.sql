-- sql10
CREATE TABLE IF NOT EXISTS sql10 (
    c_custkey INT NOT NULL,
    c_name VARCHAR(25) NOT NULL,
    revenue DECIMAL(18, 2) NOT NULL,
    c_acctbal DECIMAL(18, 2) NOT NULL,
    n_name VARCHAR(25) NOT NULL,
    c_address VARCHAR(40) NOT NULL,
    c_phone VARCHAR(15) NOT NULL,
    c_comment VARCHAR(117) NOT NULL
);

TRUNCATE TABLE sql10;

INSERT INTO sql10
select
    c_custkey,
    c_name,
    sum(l_extendedprice * (1 - l_discount)) as revenue,
    c_acctbal,
    n_name,
    c_address,
    c_phone,
    c_comment
from
    customer,
    orders,
    lineitem,
    nation
where
    c_custkey = o_custkey
    and l_orderkey = o_orderkey
    and o_orderdate >= date '1993-10-01'
    and o_orderdate < date '1994-01-01'
    and l_returnflag = 'R'
    and c_nationkey = n_nationkey
group by
    c_custkey,
    c_name,
    c_acctbal,
    c_phone,
    n_name,
    c_address,
    c_comment
order by
    revenue desc;   

select count(*) from sql10;