import os
import configparser

CONFIG_PARA = ['mode', 'scalefactor', 'islineitem', 
               'isorders', 'iscustomer', 'ispartsupp',
               'ispart', 'issupplier', 'isnation', 'isregion']
TABLES_FOLDER_PATH = '/mnt/e/projects/Cquirrel_implement/resource/tpch'
CONFIG_FOLDER_PATH = "/mnt/e/projects/Cquirrel_implement/resource/config"
LOG_FOLDER_PATH = "/mnt/e/projects/Cquirrel_implement/resource/logs"
CONFIG_FILE_NAME = "config_4_FIFO.ini"
conf = configparser.ConfigParser()
config_file_name = os.path.join(CONFIG_FOLDER_PATH, CONFIG_FILE_NAME)
print(config_file_name)
if not os.path.exists(config_file_name):
    raise FileNotFoundError('config file not found.')
conf.read(config_file_name, encoding='UTF-8')
# select the section DEFAULT
config = conf['DEFAULT']
config_list = [x for x in config]
# check if the key of config are fully correct
if config_list.sort() != CONFIG_PARA.sort():
    raise Exception("config parameters should contain 'mode', 'scalefactor', 'islineitem', "
                    "'isorders', 'iscustomer', 'ispartsupp', 'ispart', 'issupplier', 'isnation', 'isregion'.")
# log settings
log_file_path = os.path.join(LOG_FOLDER_PATH, "log_{}_{}.txt".format(config['Mode'], config['ScaleFactor']))
log_file = open(log_file_path, "w")
log_file.write("config_file_name: {}\n".format(config_file_name))
def data_generator(config):
    # read the settings from file
    scale_factor = config.getfloat('ScaleFactor')
    if scale_factor >= 1:
        scale_factor = config.getint('ScaleFactor')
        # raise ValueError("scale factor should be positive.")
    print("scale_factor:", scale_factor)
    log_file.write("scale_factor: {}\n".format(scale_factor))
    mode = config['Mode']
    if mode != 'insertOnly' and mode != 'FIFO':
        raise ValueError("mode should be insertOnly or FIFO.")

    isLineitem = config.getboolean('isLineitem')
    isOrders = config.getboolean('isOrders')
    isCustomer = config.getboolean('isCustomer')
    isPartSupp = config.getboolean('isPartSupp')
    isPart = config.getboolean('isPart')
    isSupplier = config.getboolean('isSupplier')
    isNation = config.getboolean('isNation')
    isRegion = config.getboolean('isRegion')
    
    # input data file path prefix
    data_file_path_prefix = os.path.join(TABLES_FOLDER_PATH, str(scale_factor))
    print("data_file_path_prefix:",data_file_path_prefix)
    log_file.write("data_file_path_prefix: {}\n".format(data_file_path_prefix))
    if not os.path.exists(data_file_path_prefix):
        raise Exception("data file path does not exists.")
    # set the output file
    output_file_path = os.path.join(data_file_path_prefix, "input_data_{}_{}.csv".format(mode, scale_factor))
    output = open(output_file_path, "w")
    
    # define a output func to write data to file
    def write_to_output_and_kafka(s):
        output.write(s)

    # set the size of different tables
    lineitem_size = scale_factor * 6000000
    orders_size = scale_factor * 1500000
    nation_size = 25
    region_size = 5
    partsupp_size = scale_factor * 800000
    part_size = scale_factor * 200000
    supplier_size = scale_factor * 10000
    customer_size = scale_factor * 150000

    tpch_tables = ['customer', 'lineitem', 'nation', 'orders', 'part', 'partsupp', 'region', 'supplier']
    tpch_tables_lines_num = [customer_size, lineitem_size, nation_size, orders_size, part_size, partsupp_size,
                             region_size, supplier_size]
    
    
    if scale_factor >= 1:
        tpch_tables_path = [os.path.join(data_file_path_prefix, x + ".tbl") for x in tpch_tables]
    else:
        tpch_tables_path = [os.path.join(TABLES_FOLDER_PATH,'1', x + ".tbl") for x in tpch_tables]
    # check if the files exists or not
    for ttp in tpch_tables_path:
        if not os.path.exists(ttp):
            raise FileNotFoundError("{} not found.".format(ttp))
    # check if the files are null
    for ttp in tpch_tables_path:
        if not os.path.getsize(ttp):
            raise Exception("{} is an empty file.".format(ttp))
    # check the lines number of files
    print("*************************************")
    log_file.write("check the lines number of files:\n")
    # for index in range(len(tpch_tables_path)):
    #     with open(tpch_tables_path[index], 'r') as f:
    #         lines_num = len(f.readlines())
    #         tpch_tables_lines_num[index] = lines_num
    #         print("{} has {} lines".format(tpch_tables_path[index], lines_num))
    #         log_file.write("{} has {} lines\n".format(tpch_tables_path[index], lines_num))

    if mode == 'insertOnly':
        window_size = tpch_tables_lines_num[tpch_tables.index('lineitem')]
    elif mode == 'FIFO':
        window_size = 6000000*scale_factor*0.2
    else:
        raise ValueError("mode should be insertOnly or FIFO.")
    # open the files
    if scale_factor >= 1:
        lineitem = open(os.path.join(data_file_path_prefix, "lineitem.tbl"), "r")
        orders = open(os.path.join(data_file_path_prefix, "orders.tbl"), "r")
        partsupp = open(os.path.join(data_file_path_prefix, "partsupp.tbl"), "r")
        part = open(os.path.join(data_file_path_prefix, "part.tbl"), "r")
        supplier = open(os.path.join(data_file_path_prefix, "supplier.tbl"), "r")
        customer = open(os.path.join(data_file_path_prefix, "customer.tbl"), "r")
        nation = open(os.path.join(data_file_path_prefix, "nation.tbl"), "r")
        region = open(os.path.join(data_file_path_prefix, "region.tbl"), "r")

        # delete = (window_size != 0)
        lineitem_d = open(os.path.join(data_file_path_prefix, "lineitem.tbl"), "r")
        orders_d = open(os.path.join(data_file_path_prefix, "orders.tbl"), "r")#
        partsupp_d = open(os.path.join(data_file_path_prefix, "partsupp.tbl"), "r")#
        part_d = open(os.path.join(data_file_path_prefix, "part.tbl"), "r")#
        supplier_d = open(os.path.join(data_file_path_prefix, "supplier.tbl"), "r")#
        customer_d = open(os.path.join(data_file_path_prefix, "customer.tbl"), "r")#
        nation_d = open(os.path.join(data_file_path_prefix, "nation.tbl"), "r")#
        region_d = open(os.path.join(data_file_path_prefix, "region.tbl"), "r")#
    else:
        lineitem = open(os.path.join(TABLES_FOLDER_PATH,'1', "lineitem.tbl"), "r")
        orders = open(os.path.join(TABLES_FOLDER_PATH,'1', "orders.tbl"), "r")
        partsupp = open(os.path.join(TABLES_FOLDER_PATH,'1', "partsupp.tbl"), "r")
        part = open(os.path.join(TABLES_FOLDER_PATH,'1', "part.tbl"), "r")
        supplier = open(os.path.join(TABLES_FOLDER_PATH,'1', "supplier.tbl"), "r")
        customer = open(os.path.join(TABLES_FOLDER_PATH,'1', "customer.tbl"), "r")
        nation = open(os.path.join(TABLES_FOLDER_PATH,'1', "nation.tbl"), "r")
        region = open(os.path.join(TABLES_FOLDER_PATH,'1', "region.tbl"), "r")

        # delete = (window_size != 0)
        lineitem_d = open(os.path.join(TABLES_FOLDER_PATH,'1', "lineitem.tbl"), "r")
        orders_d = open(os.path.join(TABLES_FOLDER_PATH,'1', "orders.tbl"), "r")#
        partsupp_d = open(os.path.join(TABLES_FOLDER_PATH,'1', "partsupp.tbl"), "r")#
        part_d = open(os.path.join(TABLES_FOLDER_PATH,'1', "part.tbl"), "r")#
        supplier_d = open(os.path.join(TABLES_FOLDER_PATH,'1', "supplier.tbl"), "r")#
        customer_d = open(os.path.join(TABLES_FOLDER_PATH,'1', "customer.tbl"), "r")#
        nation_d = open(os.path.join(TABLES_FOLDER_PATH,'1', "nation.tbl"), "r")#
        region_d = open(os.path.join(TABLES_FOLDER_PATH,'1', "region.tbl"), "r")#
   
    # init the count number
    count = 0
    delete_count = 0 - window_size
    part_count = 0
    part_delete_count = 0
    supplier_count = 0
    supplier_delete_count = 0
    orders_count = 0
    orders_delete_count = 0
    customer_count = 0
    customer_delete_count = 0
    partsupp_count = 0
    partsupp_delete_count = 0
    nation_count = 0
    nation_delete_count = 0
    region_count = 0
    region_delete_count = 0

    # read the first line
    line_lineitem = lineitem.readline()
    line_lineitem_d = lineitem_d.readline()
    line_orders = orders.readline()
    line_orders_d = orders_d.readline()
    line_partsupp = partsupp.readline()
    line_partsupp_d = partsupp_d.readline()
    line_part = part.readline()
    line_part_d = part_d.readline()
    line_supplier = supplier.readline()
    line_supplier_d = supplier_d.readline()
    line_customer = customer.readline()
    line_customer_d = customer_d.readline()
    line_nation = nation.readline()
    line_nation_d = nation_d.readline()
    line_region = region.readline()
    line_region_d = region_d.readline()

    # final window
    lineItem_window = []
    orders_window = []
    customer_window = []
    partsupp_window = []
    part_window = []
    supplier_window = []
    nation_window = []
    region_window = []
    # write the first part
    last_progress_milestone=0
    while line_lineitem :
        if scale_factor < 1 and count >= lineitem_size:
            break
        count = count + 1
        delete_count = delete_count + 1
        current_milestone = int(count / lineitem_size * 10)
        if current_milestone > last_progress_milestone:
            print(f"Progress: {current_milestone * 10}%")
            last_progress_milestone = current_milestone
        if isLineitem:
            if mode == 'FIFO' and scale_factor == 1:
                lineItem_window.append(line_lineitem)
            write_to_output_and_kafka("+LI" + line_lineitem)
        line_lineitem = lineitem.readline()
        if delete_count > 0:
            if isLineitem:
                if mode == 'FIFO' and scale_factor == 1:
                    lineItem_window.pop(0)
                write_to_output_and_kafka("-LI" + line_lineitem_d)
            line_lineitem_d = lineitem_d.readline()

        if count * orders_size / lineitem_size > orders_count and line_orders:
            orders_count = orders_count + 1
            if isOrders:
                if mode == 'FIFO' and scale_factor == 1:
                    orders_window.append(line_orders)
                write_to_output_and_kafka("+OR" + line_orders)
            line_orders = orders.readline()
            if delete_count * orders_size / lineitem_size > orders_delete_count and line_orders_d:
                orders_delete_count = orders_delete_count + 1
                if isOrders:
                    if mode == 'FIFO' and scale_factor == 1:
                        orders_window.pop(0)
                    write_to_output_and_kafka("-OR" + line_orders_d)
                line_orders_d = orders_d.readline()

        if count * customer_size / lineitem_size > customer_count and line_customer:
            customer_count = customer_count + 1
            if isCustomer:
                if mode == 'FIFO' and scale_factor == 1:
                    customer_window.append(line_customer)
                write_to_output_and_kafka("+CU" + line_customer)
            line_customer = customer.readline()
            if delete_count * customer_size / lineitem_size > customer_delete_count and line_customer_d:
                customer_delete_count = customer_delete_count + 1
                if isCustomer:
                    if mode == 'FIFO' and scale_factor == 1:
                        customer_window.pop(0)
                    write_to_output_and_kafka("-CU" + line_customer_d)
                line_customer_d = customer_d.readline()

        if count * part_size / lineitem_size > part_count and line_part:
            part_count = part_count + 1
            if isPart:
                if mode == 'FIFO' and scale_factor == 1:
                    part_window.append(line_part)
                write_to_output_and_kafka("+PA" + line_part)
            line_part = part.readline()
            if delete_count * part_size / lineitem_size > part_delete_count and line_part_d:
                part_delete_count = part_delete_count + 1
                if isPart:
                    if mode == 'FIFO' and scale_factor == 1:
                        part_window.pop(0)
                    write_to_output_and_kafka("-PA" + line_part_d)
                line_part_d = part_d.readline()

        if count * supplier_size / lineitem_size > supplier_count and line_supplier:
            supplier_count = supplier_count + 1
            if isSupplier:
                if mode == 'FIFO' and scale_factor == 1:
                    supplier_window.append(line_supplier)
                write_to_output_and_kafka("+SU" + line_supplier)
            line_supplier = supplier.readline()
            if delete_count * supplier_size / lineitem_size > supplier_delete_count and line_supplier_d:
                supplier_delete_count = supplier_delete_count + 1
                if isSupplier:
                    if mode == 'FIFO'  and scale_factor == 1:
                        supplier_window.pop(0)
                    write_to_output_and_kafka("-SU" + line_supplier_d)
                line_supplier_d = supplier_d.readline()

        if count * partsupp_size / lineitem_size > partsupp_count and line_partsupp:
            partsupp_count = partsupp_count + 1
            if isPartSupp:
                if mode == 'FIFO' and scale_factor == 1:
                    partsupp_window.append(line_partsupp)
                write_to_output_and_kafka("+PS" + line_partsupp)
            line_partsupp = partsupp.readline()
            if delete_count * partsupp_size / lineitem_size > partsupp_delete_count and line_partsupp_d:
                partsupp_delete_count = partsupp_delete_count + 1
                if isPartSupp:
                    if mode == 'FIFO'  and scale_factor == 1:
                        partsupp_window.pop(0)
                    write_to_output_and_kafka("-PS" + line_partsupp_d)
                line_partsupp_d = partsupp_d.readline()

        if count * nation_size / lineitem_size > nation_count and line_nation:
            nation_count = nation_count + 1
            if isNation:
                if mode == 'FIFO' and scale_factor == 1:
                    nation_window.append(line_nation)
                write_to_output_and_kafka("+NA" + line_nation)
            line_nation = nation.readline()
            if delete_count * nation_size / lineitem_size > nation_delete_count and line_nation_d:
                nation_delete_count = nation_delete_count + 1
                if isNation:
                    if mode == 'FIFO'  and scale_factor == 1:
                        nation_window.pop(0)
                    write_to_output_and_kafka("-NA" + line_nation_d)
                line_nation_d = nation_d.readline()

        if count * region_size / lineitem_size > region_count and line_region:
            region_count = region_count + 1
            if isRegion:
                if mode == 'FIFO'and scale_factor == 1:
                    region_window.append(line_region)
                write_to_output_and_kafka("+RI" + line_region)
            line_region = region.readline()
            if delete_count * region_size / lineitem_size > region_delete_count and line_region_d:
                region_delete_count = region_delete_count + 1
                if isRegion:
                    if mode == 'FIFO'  and scale_factor == 1:
                        region_window.pop(0)
                    write_to_output_and_kafka("-RI" + line_region_d)
                line_region_d = region_d.readline()

    # close the file
    lineitem.close()
    orders.close()
    partsupp.close()
    part.close()
    supplier.close()
    customer.close()
    nation.close()
    region.close()

    lineitem_d.close()
    orders_d.close()
    partsupp_d.close()
    part_d.close()
    supplier_d.close()
    customer_d.close()
    nation_d.close()
    region_d.close()

    output.close()

    print("")
    print("*************************************")
    log_file.write("*************************************\n")
    out_sum=0
    if isLineitem:
        out_sum += count+delete_count
        print("count: ", count)
        print("delete_count: ", delete_count)
        log_file.write("count: {}\n".format(count))
        log_file.write("delete_count: {}\n".format(delete_count))
    
    if isCustomer:
        out_sum += customer_count+customer_delete_count
        print("customer_count: ", customer_count)
        print("customer_delete_count: ", customer_delete_count)
        log_file.write("customer_count: {}\n".format(customer_count))
        log_file.write("customer_delete_count: {}\n".format(customer_delete_count))
    
    if isNation:
        out_sum += nation_count+nation_delete_count
        print("nation_count: ", nation_count)
        print("nation_delete_count: ", nation_delete_count)
        log_file.write("nation_count: {}\n".format(nation_count))
        log_file.write("nation_delete_count: {}\n".format(nation_delete_count))
    
    if isOrders:
        out_sum += orders_count+orders_delete_count
        print("orders_count: ", orders_count)
        print("orders_delete_count: ", orders_delete_count)
        log_file.write("orders_count: {}\n".format(orders_count))
        log_file.write("orders_delete_count: {}\n".format(orders_delete_count))
    
    if isPart:
        out_sum += part_count+part_delete_count
        print("part_count: ", part_count)
        print("part_delete_count: ", part_delete_count)
        log_file.write("part_count: {}\n".format(part_count))
        log_file.write("part_delete_count: {}\n".format(part_delete_count))
    
    if isPartSupp:
        out_sum += partsupp_count+partsupp_delete_count
        print("partsupp_count: ", partsupp_count)
        print("partsupp_delete_count: ", partsupp_delete_count)
        log_file.write("partsupp_count: {}\n".format(partsupp_count))
        log_file.write("partsupp_delete_count: {}\n".format(partsupp_delete_count))
    
    if isRegion:
        out_sum += region_count+region_delete_count
        print("region_count: ", region_count)
        print("region_delete_count: ", region_delete_count)
        log_file.write("region_count: {}\n".format(region_count))
        log_file.write("region_delete_count: {}\n".format(region_delete_count))
    
    if isSupplier:
        out_sum += supplier_count+supplier_delete_count
        print("supplier_count: ", supplier_count)
        print("supplier_delete_count: ", supplier_delete_count)
        log_file.write("supplier_count: {}\n".format(supplier_count))
        log_file.write("supplier_delete_count: {}\n".format(supplier_delete_count))

    print("\ntotal count: ", out_sum)
    log_file.write("\ntotal count: {}\n".format(out_sum))
    with open(output_file_path, 'r') as f:
        res_lines_num = len(f.readlines())
    print("output file lines number: ", res_lines_num)
    print("finished: ", config_file_name)
    print("outputfile: ", output_file_path)

    log_file.write("output file lines number: {}\n".format(res_lines_num))
    log_file.write("finished: {}\n".format(config_file_name))
    log_file.write("outputfile: {}\n".format(output_file_path))
    if mode=='FIFO' and scale_factor == 1:
        print("\n=== Save Window Data===")
        log_file.write("\n=== Save Window Data===\n")
        WINDOW_FOLDER_PATH=os.path.join(data_file_path_prefix, "window_data")
        log_file.write("window folder path: {}\n".format(WINDOW_FOLDER_PATH))
        if not os.path.exists(WINDOW_FOLDER_PATH):
            os.makedirs(WINDOW_FOLDER_PATH)
        def save_window_data(window, file_name):
            if(not window):
                return
            log_file.write("save {} with {} lines\n".format(file_name, len(window)))
            with open(os.path.join(WINDOW_FOLDER_PATH, file_name), "w") as f:
                for line in window:
                    f.write(line)

        save_window_data(lineItem_window, "lineitem_window.tbl")
        save_window_data(orders_window, "orders_window.tbl")
        save_window_data(customer_window, "customer_window.tbl")
        save_window_data(partsupp_window, "partsupp_window.tbl")
        save_window_data(part_window, "part_window.tbl")
        save_window_data(supplier_window, "supplier_window.tbl")
        save_window_data(nation_window, "nation_window.tbl")
        save_window_data(region_window, "region_window.tbl")
    
    
if __name__ == '__main__':
    import time

    start = time.time()
    data_generator(config)
    end = time.time()
    print("cpu time: ", end - start)
    log_file.write("cpu time: {}\n".format(end - start))
    log_file.close()

