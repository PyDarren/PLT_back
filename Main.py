from FCS import Fcs
from FCS import StainFcs
from FCS import Write
from tkinter import filedialog
import random
import os


# 选择路径
Fpath = filedialog.askdirectory()
for file in [file for file in os.listdir(Fpath) if os.path.splitext(file)[1] == ".fcs"]:
    filename = Fpath + '/' + file

    # fcs = Fcs(filename)

    # # 写到excel中
    # fcs.fcs2excel()

    # 染色通道
    stain_fcs = StainFcs(filename)
    stain_fcs.fcs2excel(folder_name="Stain_excel")

    # # 写出到fcs中
    # save_dir = fcs.file_dir + "/WriteFcs"
    # # excel文件夹不存在时创建
    # if not os.path.exists(save_dir):
    #     os.makedirs(save_dir)
    # filename = save_dir + '/' + file
    #
    # channel_name = [par.par_short_name for par in fcs.pars]
    # marker_name = [par.par_name for par in fcs.pars]
    # data = [par.data for par in fcs.pars]
    # Write(filename, channel_name, marker_name, data)
    #
    # # 删除指定通道写出
    # fcs.delete_channel("beadDist", 105, 104, 115)

    # # 模拟提供[通道名，通道stain_name, 通道data]
    # events = int(fcs.header.info["$TOT"])
    # add_channel = list()
    # for i in range(1, 6):
    #     channel_name = "new%d" % i
    #     marker_name = "new%d" % i
    #     channel_data = [random.randint(0, 100) for event in range(0, events)]
    #     add_channel.append((channel_name, marker_name, channel_data))
    # add_channel = tuple(add_channel)
    # # 添加模拟通道写出
    # fcs.add_channel(*add_channel)
    #
    # # 修改marker_name
    # fcs.marker_rename((115, "cd++++3"), (116, "test_11"))

# Fcs.panel_rename()


