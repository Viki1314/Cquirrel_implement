import os
import configparser
import subprocess
CODEGEN_FILE = "/mnt/e/projects/Cquirrel_implement/resource/codegen.jar"
JAR2SQL_FOLDER_PATH = "/mnt/e/projects/Cquirrel_implement/resource/jar2sql"
CONFIG_FOLDER_PATH = "/mnt/e/projects/Cquirrel_implement/resource/config"
CONFIG_FILE_NAME = "config_4_FIFO.ini"
LOG_FOLDER_PATH = "/mnt/e/projects/Cquirrel_implement/resource/logs"
conf = configparser.ConfigParser()
config_file_name = os.path.join(CONFIG_FOLDER_PATH, CONFIG_FILE_NAME)
print(config_file_name)
if not os.path.exists(config_file_name):
    raise FileNotFoundError('config file not found.')
conf.read(config_file_name, encoding='UTF-8')
print(conf)
config = conf['DEFAULT']
MODE = config['Mode']
SF = config.get('ScaleFactor')
JAR2SQL_FILE_PATH = os.path.join(JAR2SQL_FOLDER_PATH,MODE,SF)
GENERATED_JSON_FILE=os.path.join(JAR2SQL_FILE_PATH, "generated.json")

INPUT_DATA_FILE=os.path.join("/mnt/e/projects/Cquirrel_implement/resource/tpch",SF,"input_data_{}_{}.csv".format(MODE, SF))
OUTPUT_DATA_FILE=os.path.join("/mnt/e/projects/Cquirrel_implement/resource/flink_result",SF,"flink_output_data_{}_{}.csv".format(MODE, SF))
INFORMATION_JSON_FILE=os.path.join(JAR2SQL_FILE_PATH, "information.json")
log_file_path = os.path.join(LOG_FOLDER_PATH, "sql2jar_log_{}_{}.txt".format(MODE, SF))
log_file = open(log_file_path, "w")
log_file.write("config_file_name: {}\n".format(config_file_name))
def r_run_codegen_to_generate_jar2(sql_content):
    if not os.path.exists(CODEGEN_FILE):
        raise FileNotFoundError('codegen.jar file not found.')
    if not os.path.exists(INPUT_DATA_FILE):
        raise FileNotFoundError('input data file not found.')
    if not os.path.exists(JAR2SQL_FILE_PATH):
        os.makedirs(JAR2SQL_FILE_PATH)
    if not os.path.exists(os.path.dirname(OUTPUT_DATA_FILE)):
        os.makedirs(os.path.dirname(OUTPUT_DATA_FILE))

    
    cmd_str = 'java -jar' + ' ' + CODEGEN_FILE \
                + ' -j ' + GENERATED_JSON_FILE \
                + ' -g ' + JAR2SQL_FILE_PATH \
                + ' -i ' + 'file://' + INPUT_DATA_FILE \
                + ' -o ' + 'file://' + OUTPUT_DATA_FILE \
                + ' -s '  + 'file ' \
                + ' -q ' + '"' + sql_content + '"'
    print("codegen command: " + cmd_str)
    log_file.write("codegen command: " + cmd_str + "\n")
    ret = subprocess.run(cmd_str, shell=True, capture_output=True)
    codegen_log_stdout = str(ret.stdout, encoding="utf-8") + "\n"
    codegen_log_stderr = str(ret.stderr, encoding="utf-8") + "\n"
    codegen_log_result = codegen_log_stdout + codegen_log_stderr
    log_file.write("codegen_log_result: " + codegen_log_result + "\n")
    
    print('codegen_log_result: ' + codegen_log_result)

    information_data = ""
    with open(INFORMATION_JSON_FILE, 'r') as f:
        data = f.readlines()
    for line in data:
        information_data = information_data + line
    log_file.write("information data: " + information_data + "\n")

q10 = """select
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
and o_orderdate >= date '[DATE1]'
and o_orderdate < date '[DATE2]'
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
revenue desc;"""

# q10 = q10.replace("[REGION]", "ASIA")
q10 = q10.replace("[DATE1]", "1993-10-01")
q10 = q10.replace("[DATE2]", "1994-01-01")
q10 = q10.replace("\n", " ")
r_run_codegen_to_generate_jar2(q10)