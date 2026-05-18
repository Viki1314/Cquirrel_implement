# Cquirrel_implement
This is the experience of the Cquirrel Demonstration on Q10,where '[DATE]' is '1993-10-01'.
```sql
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
  and o_orderdate >= date '[DATE]'
  and o_orderdate < date '[DATE]' + interval '3' month
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
```
## Environment Requirement
### Operating System
I run the experience in Windows wsl2.
### Software Dependencies
Here are the software version in which we run the cquirrel experience.
- java 1.8 !!!

<!-- Python 3.8.5  

Scala 2.12.13
Maven 3.6.3   
sbt 1.3.13  
yarn 1.22.10  
Flink 1.11.2
- flink 2.22
- python 3.12.3

- scala 2.11.12
- maven 3.8.7
- sbt
- yarn 1.22.22
- gcc 13.3.0
- node 18.19.1 -->
## Directory Description
* `mycode/DataGenerator.py` : This is the tool to generate our input data files from TPCH tables. We can edit config file to meet our requirements for the input data.
* `resource/codegen.jar` : This is the codegen components, which can transform a sql to a flink program.
## Running Steps
### Generate the input data
1. Download the [TPC-H](http://tpc.org/tpc_documents_current_versions/current_specifications5.asp) Tools and unzip it. Then you will get a directory which contains `dbgen`, `dev-tools`, and `specification.pdf`, etc.

3. Copy the `makefile.suite` file in the `dbgen` directory to `makefile`, for the purpose of suiting your own operating system and platforms. 
`> cd dbgen`
`> cp makefile.suite makefile`

4. Edit the `makefile` to suit your own environment. However, we should make sure that the data in the generated `*.tbl` file should be seperated by `"|"`. Perhaps you might need to revise the source code of the `tpc-h_tools`. Take my example:
    ```
    ################
    ## CHANGE NAME OF ANSI COMPILER HERE
    ################
    CC      = gcc
    # Current values for DATABASE are: INFORMIX, DB2, TDAT (Teradata)
    #                                  SQLSERVER, SYBASE, ORACLE, VECTORWISE
    # Current values for MACHINE are:  ATT, DOS, HP, IBM, ICL, MVS, 
    #                                  SGI, SUN, U2200, VMS, LINUX, WIN32 
    # Current values for WORKLOAD are:  TPCH
    DATABASE= ORACLE 
    MACHINE = LINUX
    WORKLOAD = TPCH
    ```

5. In the `dbgen` directory, run `make` to compile the source code, and we can get an executable file which also called `dbgen`.  
`> make makefile`

6. In the `dbgen` directory, run the `dbgen` executable file to generate `.tbl` data files. The `-s` means the size of generated data. The `-s 1` means that it will generate 1GB data. And copy all `.tbl` data file into the `DemoTools/DataGenerator` directory
    ```bash
    # 1GB data
    ./dbgen -s 1 -vf
    cp *.tbl /mnt/e/projects/Cquirrel_implement/resource/tpch/1
    # 2GB data
    ./dbgen -s 2 -vf
    cp *.tbl /mnt/e/projects/Cquirrel_implement/resource/tpch/2
    # 4GB data
    ./dbgen -s 4 -vf
    cp *.tbl /mnt/e/projects/Cquirrel_implement/resource/tpch/4
    ```

8. In the `mycode/DataGenerator.py`, generate the input data. The config files are in `resource/config` directory. The generation logs are in `resource/logs` directory.The output file are in `resource/tpch/{SF}` directory.(Requirement:sql should not contain date computation,like 'date '[DATE]' + interval '3' month')
  ```bash 
  python mycode/DataGenerator.py
  ```
### sql2jar
use `resource/codegen.jar` to transfer sql query to `generated-code-1.0-SNAPSHOT-jar-with-dependencies.jar` for flink.
  ```bash
  python mycode/sql2jar.py
  ```
### Boot the Apache Flink
1. Download the Apache Flink and unzip the package into your computer. 
2. Change the directory into `flink-1.11.2`, and start the flink cluster.  
  ```bash
  cd /mnt/e/software/flink1/flink-1.11.2/flink-1.11.2
  bash bin/start-cluster.sh
  ```
3. run flink
```bash
/mnt/e/software/flink1/flink-1.11.2/bin/flink run /mnt/d/SCUT/HK_Msc/HKUST_IT/ip_flink/Cquirrel_implement/app/generated-code/target/generated-code-1.0-SNAPSHOT-jar-with-dependencies.jar
```
### Clean output data

### Prepare mysql
1. login mysql:
`sudo mysql -u root -p`
2. create 3 databases;
  ```sql
  CREATE DATABASE tpch1;
  CREATE DATABASE tpch2;
  CREATE DATABASE tpch4;
  show databases;
  use tpch1;
  ```
  3. create tables in mysql:
  `source /mnt/e/projects/Cquirrel_implement/myCode/tpch_schema.sql`
  4. load tpch data: