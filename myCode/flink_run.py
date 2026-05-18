import os
import configparser
import subprocess
FLINK_HOME = "/mnt/e/software/flink1/flink-1.11.2/bin/flink"
CONFIG_FOLDER_PATH = "/mnt/e/projects/Cquirrel_implement/resource/config"
# read config file to get the sql content
conf = configparser.ConfigParser()
config_file_name = "config_1_FIFO.ini"
print(config_file_name)
if not os.path.exists(os.path.join(CONFIG_FOLDER_PATH, config_file_name)):
    raise FileNotFoundError('config file not found.')
conf.read( os.path.join(CONFIG_FOLDER_PATH, config_file_name), encoding='UTF-8')
print(conf)
config = conf['DEFAULT']
MODE = config['Mode']
SF = config.get('ScaleFactor')

# log
log_folder_path = "/mnt/e/projects/Cquirrel_implement/resource/logs"
log_file_path = os.path.join(log_folder_path, "flink_run_log_{}_{}.txt".format(MODE, SF))

jar_file_path = "/mnt/e/projects/Cquirrel_implement/resource/jar2sql/{}/{}/generated-code/target/generated-code-1.0-SNAPSHOT-jar-with-dependencies.jar".format(MODE, SF)
cmd_str = FLINK_HOME + " run "+ jar_file_path
print("flink run command: " + cmd_str)

with open(log_file_path, "w", encoding='utf-8') as log_file:
    log_file.write(f"flink run command: {cmd_str}\n")
    log_file.flush()
    
    try:
        
        process = subprocess.Popen(
            cmd_str,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  
            text=True,                 
            bufsize=1                  
        )
        
       
        for line in process.stdout:
            print(line, end="")        
            log_file.write(line)       
            log_file.flush()           
            
        return_code = process.wait()
        
        if return_code == 0:
            success_msg = "\n================ Flink 任务提交并执行成功 ================\n"
            print(success_msg)
            log_file.write(success_msg)
        else:
            error_msg = f"\n❌ Flink 任务异常退出，Linux 错误码: {return_code}\n"
            print(error_msg)
            log_file.write(error_msg)

    except Exception as e:
        exception_msg = f"\n💥 脚本流处理执行期间发生异常: {str(e)}\n"
        print(exception_msg)
        log_file.write(exception_msg)