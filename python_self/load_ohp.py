import os
import sys
from MysqlTool import MysqlTool

import numpy as np
from lxproduct.io import load_dataset


def get_cappi_data_2d(filein):
    """
        读取cappi数据, 输入路径为: filein
        返回: lon, lat, ohp
    """
    data = load_dataset(filein)
    phi = data.blocks[0]
    val = np.array(data.__dict__.get(phi).data).astype(np.float32)
    lon = np.array(data.__dict__.get(phi).dimension_values[1])
    lat = np.array(data.__dict__.get(phi).dimension_values[0])
    # 注释掉0值处理
    # fill_value = data.__dict__.get(phi).fill_value
    # val[val == fill_value] = np.nan
    print(lon.shape, lat.shape, val.shape)
    y, x = val.shape
    result = []
    for i_x in range(x):
        for i_y in range(y):
            result.append((str(lon[i_x]), str(lat[i_y]), str(val[i_y, i_x])))
    return result


def save_to_file(data_list, f_name: str = 'result.txt'):
    """
    将数据列表保存到文件
    :param data_list: 数据列表
    :param f_name: 文件名参数，默认为result.txt
    :return:
    """
    f = open(f_name, "w")
    f.writelines(data_list)
    f.close()


def save_to_mysql(data_list):
    """
    将数据列表保存到数据库
    :param data_list: 数据列表
    :return:
    """
    sql = "insert into ohp_info (lon,lat,ohp) values (%s, %s, %s)"
    with MysqlTool() as session:
        session.insert_batch(sql=sql, args=data_list)


def print_to_file(ohp_path, f_name):
    save_to_file(get_cappi_data_2d(ohp_path), f_name)


def print_to_mysql(ohp_path):
    save_to_mysql(get_cappi_data_2d(ohp_path))


if __name__ == '__main__':
    # print_to_file("SHAA_20240619163000_OHP_L.dat", "ohp_l.txt")
    # print_to_file("SHAA_20240619163000_OHP.dat", "ohp.txt")
    # print_to_mysql("SHAA_20240619163000_OHP_L.dat")
    print_to_mysql("SHAA_20240619163000_OHP.dat")
