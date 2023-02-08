# -*- coding : utf-8 -*-
import os
from hdfs import InsecureClient

# hdfs 目标路径
base_path = "/MITRE_ATTACK_DATA"
# 本地需要上传的路径（相对路径）
local_dir = "./"

client_hdfs = InsecureClient('http://192.168.73.169:9870', user='reptile')
client_hdfs.makedirs(base_path)


def upload_train_data(path: str) -> None:
    """
    :param path: relative path of train data
    :return: none
    """
    file_name = "description_data.txt"
    local_path = os.path.join(path, file_name).replace("\\", "/")  # relative path of all files
    print(local_path)
    hdfs_path = base_path + "/" + file_name  # absolute path in hdfs
    print(hdfs_path)

    client_hdfs.upload(hdfs_path, local_path)
    print("file:", file_name)


if __name__ == '__main__':
    upload_train_data(local_dir)
