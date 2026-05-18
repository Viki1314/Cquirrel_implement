import re
import csv
import configparser
import os

# parameters
config_file_name = "config_1_insertOnly.ini"

# constants
INPUF_FILE_DIR= "/mnt/e/projects/Cquirrel_implement/resource/flink_result"
CONFIG_FOLDER_PATH = "/mnt/e/projects/Cquirrel_implement/resource/config"

# read config file to get the sql content
conf = configparser.ConfigParser()
print(config_file_name)
if not os.path.exists(os.path.join(CONFIG_FOLDER_PATH, config_file_name)):
    raise FileNotFoundError('config file not found.')
conf.read( os.path.join(CONFIG_FOLDER_PATH, config_file_name), encoding='UTF-8')
print(conf)
config = conf['DEFAULT']
MODE = config['Mode']
SF = config.get('ScaleFactor')
input_file = os.path.join(INPUF_FILE_DIR,SF, "flink_output_data_{}_{}.csv".format(MODE, SF))
output_file = os.path.join(INPUF_FILE_DIR,SF, "flink2mysql_data_{}_{}.csv".format(MODE, SF))

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    
    writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    
    
    for line in infile:
        line = line.strip()
        if not line:
            continue
        
        # 1. 去除两端的小括号 (...)
        if line.startswith('(') and line.endswith(')'):
            line = line[1:-1]
        
        # 2. 按竖线 | 切分字段
        parts = line.split('|')
        
        # 3. 动态提取：前 7 个字段 + 倒数第 2 个字段(revenue) + 最后一个字段(timestamp)
        if len(parts) >= 9:
            c_custkey = parts[0]
            c_name = parts[1]
            c_acctbal = parts[2]
            c_phone = parts[3]
            n_name = parts[4]
            c_address = parts[5]
            c_comment = parts[6]
            revenue = parts[7]
            timestamp = parts[-1]
            
            # 组合成完整的 9 列数据
            valid_data = [c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment, revenue, timestamp]
            
            # 清理每个字段两端的空格
            valid_data = [field.strip() for field in valid_data]

            # 4. 写入标准 CSV 文件
            writer.writerow(valid_data)

print(f"清洗完成！规范化后的文件已保存至: {output_file}")