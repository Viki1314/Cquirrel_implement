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
        ROW_NUMBER() OVER (
            PARTITION BY  c_custkey, 
                    c_name, 
                    c_acctbal, 
                    c_phone, 
                    n_name, 
                    c_address, 
                    c_comment, 
                    revenue, 
                    flink_timestamp
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
SELECT
    count(1) as total_count,
    sum(if(t1.revenue is not null and abs(t1.revenue - t2.revenue) < 0.01, 1, 0)) as match_count
    -- sum(if(abs(t1.revenue - t2.revenue) < 0.01, 0, 1)) as mismatch_count
from unique_revenue t1 right join sql10 t2 on
    t1.c_custkey = t2.c_custkey and
    t1.c_name = t2.c_name and
    t1.c_acctbal = t2.c_acctbal and
    t1.c_phone = t2.c_phone and
    t1.n_name = t2.n_name and
    t1.c_address = t2.c_address and
    t1.c_comment = t2.c_comment 
;