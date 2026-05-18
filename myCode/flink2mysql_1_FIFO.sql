use tpch1_FIFO;

CREATE TABLE IF NOT EXISTS flink_sql10 (
    c_custkey INT NOT NULL,
    c_name VARCHAR(25) NOT NULL,
    c_acctbal DECIMAL(18, 2) NOT NULL,
    c_phone VARCHAR(15) NOT NULL,
    n_name VARCHAR(25) NOT NULL,
    c_address VARCHAR(40) NOT NULL,
    c_comment VARCHAR(117) NOT NULL,
    revenue DECIMAL(18, 2) NOT NULL,
    flink_timestamp BIGINT NOT NULL
);

TRUNCATE TABLE flink_sql10;

LOAD DATA INFILE '/mnt/e/projects/Cquirrel_implement/resource/flink_result/1/flink2mysql_data_FIFO_1.csv'
INTO TABLE flink_sql10
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';






