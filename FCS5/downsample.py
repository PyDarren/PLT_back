from FCS import *
from tkinter import filedialog
import os
from tkinter import Tk

# 选择路径
root = Tk()
root.withdraw()
Fpath = filedialog.askdirectory()
file_tuple = tuple([Fpath + '/' + filename for filename in os.listdir(Fpath)
                    if os.path.splitext(filename)[1] == ".fcs"])

# file = Fpath + "/MergeFcs/test.fcs"
# merge_fcs(file, *file_tuple)

# 读取panel表信息
panel_file = Fpath + "/panel.xlsx"
panel_table = Fcs.export_panel_tuple(panel_file)
print(panel_table)
rename_by_panel_table(panel_table, *file_tuple)

for filename in [filename for filename in os.listdir(Fpath) if os.path.splitext(filename)[1] == ".fcs"]:
    file = Fpath + '/' + filename
    fcs = StainFcs(file)

    pars = fcs.pars
    # 降采样
    pars = fcs.down_sample(pars, 40000)
    pars = fcs.marker_rename(pars, (115, "CD3_test"), (89, "cd45_test"))
    # 根据当前的filename去查找新的name
    new_file = Fpath + "/DownSample/" + filename
    fcs.write_to(new_file, pars)
