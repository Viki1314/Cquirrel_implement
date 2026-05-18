use tpch1;
WITH ranked_revenue AS (
    SELECT 
        c_custkey, 
        c_name, 
        c_acctbal, 
        c_phone, 
        n_name, 
        c_address, 
        c_comment, 
        revenue, 
        flink_timestamp,
        row_number() OVER (
            PARTITION BY  c_custkey, 
                    c_name, 
                    c_acctbal, 
                    c_phone, 
                    n_name, 
                    c_address, 
                    c_comment        
            ORDER BY revenue DESC
        ) AS rn
    FROM flink_sql10
),
unique_revenue AS (
    SELECT 
        c_custkey, 
        c_name, 
        c_acctbal, 
        c_phone, 
        n_name, 
        c_address, 
        c_comment, 
        revenue, 
        flink_timestamp
    FROM ranked_revenue 
    WHERE rn = 1 and revenue > 0
)
-- select count(1) as total_count ,count(distinct c_custkey, 
--         c_name, 
--         c_acctbal, 
--         c_phone, 
--         n_name, 
--         c_address, 
--         c_comment)  as unique_count
-- from unique_revenue;
SELECT
    count(1) as total_count
    ,sum(if(t1.revenue is not null and abs(t1.revenue - t2.revenue) < 0.02, 1, 0)) as match_count
    ,sum(if(t1.revenue is null, 1, 0)) as mismatch_count
from unique_revenue t1 right join sql10 t2 on
   t1.c_custkey = t2.c_custkey and
    TRIM(t1.c_name) = TRIM(t2.c_name)   and
    t1.c_acctbal = t2.c_acctbal and
    TRIM(t1.c_phone) = TRIM(t2.c_phone) and
    TRIM(t1.n_name) = TRIM(t2.n_name) and
    TRIM(t1.c_address) = TRIM(t2.c_address) and
    TRIM(t1.c_comment) = TRIM(t2.c_comment)
;
